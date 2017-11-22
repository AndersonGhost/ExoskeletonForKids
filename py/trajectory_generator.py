import build.hip as hip
import build.knee as knee
import numpy as np
import parameters as par

class TrajectoryGenerator:

    def __init__(self, t = 0, walking_angle = par._walking_angle_(), sample_time = 0.001, halfTotalTime = 1): # FIXME: the step time is set to be very small because plot is too slow
        self.t = t; 
        self.walking_angle = walking_angle
        self.sample_time = sample_time # in seconds
        self.rightStarted = 0 # the right leg has not yet started!
        self.halfTotalTime = halfTotalTime

        ### left Hip
        self.hip_trajectory_generator_l = hip.StepHipTraj()  # new object

        self.hip_trajectory_generator_l.reset()
        self.hip_trajectory_generator_l.set_max_hip_flexion( par._max_hip_flexion_() ) # degrees, default 36
        self.hip_trajectory_generator_l.set_max_hip_flexion_time( par._max_hip_flexion_time_portion_() * halfTotalTime / self.sample_time)       # in ms
        self.hip_trajectory_generator_l.set_step_time( halfTotalTime / self.sample_time ) # in ms, integer. 5000 here.
        self.hip_trajectory_generator_l.set_walking_angle( self.walking_angle ) # offset, can vary
        self.hip_trajectory_generator_l.set_swing_start( par._hip_swing_start_() ) # default -6.934
        self.hip_trajectory_generator_l.set_step_range( par._step_range_() ) # step length in meter. example: 0.78m legLen 1.1m -> theta 41.8
        self.hip_trajectory_generator_l.set_leg_length( par._leg_length_() )

        ### left Knee
        self.knee_trajectory_generator_l = knee.StepKneeTraj()  # new object

        self.knee_trajectory_generator_l.reset()
        self.knee_trajectory_generator_l.set_max_hip_flexion_time( par._max_hip_flexion_time_portion_()*halfTotalTime/self.sample_time )       # in ms
        self.knee_trajectory_generator_l.set_step_time( halfTotalTime/self.sample_time ) # in ms, integer. 5000 here.
        self.knee_trajectory_generator_l.set_max_knee_flexion( par._max_knee_flexion_() ) # in degrees
        self.knee_trajectory_generator_l.set_second_knee_flexion( par._second_knee_flexion_() )
        self.knee_trajectory_generator_l.set_min_knee_flexion( par._min_knee_flexion_() )
        self.knee_trajectory_generator_l.set_walking_angle( self.walking_angle ) 

        self.hip_trajectory_generator_l.init() # set coordinates for interpolation
        self.knee_trajectory_generator_l.init()
        ########################################
        ### right Hip
        self.hip_trajectory_generator_r = hip.StepHipTraj()  # right leg

        self.hip_trajectory_generator_r.reset()
        self.hip_trajectory_generator_r.set_max_hip_flexion( par._max_hip_flexion_() ) # degrees, default 36
        self.hip_trajectory_generator_r.set_max_hip_flexion_time( par._max_hip_flexion_time_portion_() * halfTotalTime/self.sample_time)       # in ms
        self.hip_trajectory_generator_r.set_step_time( halfTotalTime / self.sample_time ) # in ms, integer. 5000 here.
        self.hip_trajectory_generator_r.set_walking_angle( self.walking_angle )                 # offset, can vary
        self.hip_trajectory_generator_r.set_swing_start( par._hip_swing_start_() ) # default -6.934
        self.hip_trajectory_generator_r.set_step_range( par._step_range_() ) # step length in meter. example: 0.78m legLen 1.1m -> theta 41.8
        self.hip_trajectory_generator_r.set_leg_length( par._leg_length_() )

        ### right Knee
        self.knee_trajectory_generator_r = knee.StepKneeTraj()  # new object

        self.knee_trajectory_generator_r.reset()
        self.knee_trajectory_generator_r.set_max_hip_flexion_time( par._max_hip_flexion_time_portion_()*halfTotalTime/self.sample_time )       # in ms
        self.knee_trajectory_generator_r.set_step_time( halfTotalTime/self.sample_time ) # in ms, integer. 5000 here.
        self.knee_trajectory_generator_r.set_max_knee_flexion( par._max_knee_flexion_() ) # in degrees
        self.knee_trajectory_generator_r.set_second_knee_flexion( par._second_knee_flexion_() )
        self.knee_trajectory_generator_r.set_min_knee_flexion( par._min_knee_flexion_() )
        self.knee_trajectory_generator_r.set_walking_angle( self.walking_angle ) 

        self.hip_trajectory_generator_r.init() # set coordinates for interpolation
        self.knee_trajectory_generator_r.init()
        # time_array = np.arange(0, hip_trajectory_generator_l.get_step_time() 
        # * sample_time * 2, sample_time)                     # in seconds


    def generateTrajectory(self):
        done, hip_value_l = self.hip_trajectory_generator_l.Increment()
        done, knee_value_l = self.knee_trajectory_generator_l.Increment() # generate traj in next time step
        # print self.hip_trajectory_generator_l.get_time(), " ", knee_value_l
        if (self.rightStarted == 1) or (self.hip_trajectory_generator_l.get_time() > self.halfTotalTime):
            done, hip_value_r = self.hip_trajectory_generator_r.Increment()
            done, knee_value_r = self.knee_trajectory_generator_r.Increment() # generate traj in next time step
            self.rightStarted = 1
        else:
            hip_value_r = hip_value_l
            knee_value_r = knee_value_l
        
        angles = np.array([self.walking_angle, hip_value_l - self.walking_angle, knee_value_l,
                           hip_value_r - self.walking_angle, knee_value_r]) # FIXME! generate for different legs!
        return angles

    def getTime(self):
        return self.hip_trajectory_generator_l.getTime()
