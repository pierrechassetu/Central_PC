import rclpy
from rclpy.node import Node

import numpy as np
from numpy.linalg import norm
from scipy.optimize import linear_sum_assignment, minimize
import math as m
import time

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from std_msgs.msg import Bool
from interfaces.srv import Task2

from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy
from rclpy.qos import qos_profile_sensor_data

from message_filters import ApproximateTimeSynchronizer, Subscriber
from central_pc.utils import generate_points, quat2eul

DELTA = int(25*2*m.sqrt(2))+1 # r_jetbot_waveshare = 25 cm
MAX_LIN_VEL = 1. # max linear velocity in m/s
verbose = True

class centralPC(Node):
    def __init__(self, n_SycaBot, ids):
        super().__init__('central_pc')
        self.jb_positions = np.zeros((n_SycaBot,3))
        self.goals = None
        self.exec_state = Bool()
        self.init = False
        self.advertise = True
        self.time_init = time.time()
        
        self.n_sycabots = n_SycaBot
        self.OptiTrack_sub = []
        
        self.id_jb_ready = []
        self.accepted_id = ids
        
        qos = qos_profile_sensor_data
        
        # Create service for task request
        self.task_srv = self.create_service(Task2, 'task_srv', self.set_task_cb)
    
        # Create execution state topic
        self.exec_state_pub = self.create_publisher(Bool, 'exec_state', qos)
        self.timer = self.create_timer(0.5, self.set_execstate_cb)
    
    
    def set_execstate_cb(self):
        '''
        Send a start signal once all Jetbots have their assigned task, if not just send a False.
        arguments :
        ------------------------------------------------
        return :
        '''
        if len(self.id_jb_ready) == self.n_sycabots :
            self.exec_state.data = True
        else :
            self.exec_state.data = False
        # if verbose : self.get_logger().info('publishing \n')
        self.exec_state_pub.publish(self.exec_state)
        return


    def set_task_cb(self, request, response):
        '''
        Compute goals if it has never been init and give it to the asking jetbot.

        arguments :
            request (interfaces.srv/Start.Response) =
                id (int64) = identifier of the jetbot [1,2,3,...]
                position (Pose) = pose of the jetbot
        ------------------------------------------------
        return :
            response (interfaces.srv/Task.Response) = 
                task (geometry_msgs.msg/Pose) = pose of the assigned task
        '''
        self.get_logger().info('Sending task to SycaBot_W%d\n' % (request.id))
        # Step 1 : if central has never initialised goals locations, do it
        if not self.init :
            self.jb_positions[request.id-1,:] = [request.x, request.y, request.theta]
            if verbose :
                self.get_logger().info('pose : %f, %f, %f \n' % (request.x, request.y, request.theta))

            self.init = True
            k = 20
            n_goals = 0
            
            while n_goals < self.n_sycabots : # We always want more goals than jetbot for now
                self.goals = generate_points(x_bound=200,y_bound=400,r=DELTA, k=k)
                n_goals = self.goals.shape[0]
                k+=10

            while self.n_sycabots < self.goals.shape[0]: # Since we want N=M we suppress the number of remaining goals
                idx = np.random.randint(0,self.goals.shape[0])
                self.goals = np.delete(self.goals, idx,0)
            self.goals = self.goals/100
            self.cCAPT(vmax = MAX_LIN_VEL, t0=0.)

        # Step 2 : Compute and send response if id is the good one
        task = Point()
        self.get_logger().info('got request from %d\n'%(request.id))

        if request.id in self.accepted_id :
            task.x = self.goals[request.id-1][0] - 1
            task.y = self.goals[request.id-1][1] - 2
            # task.x = -1.5
            # task.y = 1.5
            task.z = 0.
            response.task = task
            if request.id not in self.id_jb_ready : self.id_jb_ready.append(request.id)
        else :
            task.x = 0.
            task.y = 0.
            task.z = 0.
        self.get_logger().info('task is : [%f,%f]\n' % (task.x ,task.y))
        return response


    def cCAPT(self, vmax=1., t0=0):
        '''
        Task assignment algorithm. c-CAPT algo adapted from the work of M. Turpin : https://journals.sagepub.com/doi/full/10.1177/0278364913515307
        Algorithm developped for the case where M = N and cost function is difference of velocities squared.

        arguments :
            vmax (float) = max speed of the robot [m/s]
            t0   (float) = initial starting time [s]
        ------------------------------------------------
        return :
        '''
        # Step 1 : initialise varibales N,M, D and phi
        N,M = self.jb_positions.shape[0], self.goals.shape[0]
        D=np.zeros((N,M))
        phi=np.zeros((N,M))
        
        # Step 2 : Compute cost matrix for each position and goal
        for i in range(N):
            for j in range(M):
                D[i,j] = norm(self.jb_positions[i,0:2] - self.goals[j])
        
        # Step 3 : Compute phi_star using a simple optimizer
        row_idx, col_idx = linear_sum_assignment(D)
        phi[row_idx, col_idx] = 1
        tf = round(max(norm(self.jb_positions[:,0:2] - self.goals[col_idx], axis=1))/vmax)


        # Step 4 : Compute trajectory and the task where goals[i] corresponds to jebtot[i]
        self.goals = phi@self.goals
        # alpha0 = -t0/(tf-t0)
        # alpha1 = 1/(tf-t0)
        # traj = np.zeros((tf,N,2))
        # for t in range(t0,tf):
        #     B = alpha0 + alpha1*(t+1)
        #     traj[t] = (1-B)*jb_positions[:,0:2] + B*(phi@goals) 
        # return traj
        return




def main(args=None):
    rclpy.init(args=args)
    ids = []
    n_sycabots = int(input("Enter number of Sycabots : "))
    
    for i in range(0, n_sycabots):
        ids.append(int(input("id n°%d : "%(i+1))))

    central = centralPC(n_sycabots, ids)

    rclpy.spin(central)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    central.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

    





