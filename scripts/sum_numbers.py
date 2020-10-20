#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16
import smach
import smach_ros
import time
class getNum(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['add','result'])
        self.counter = 0
        self.start = 0
        self.subscriber = rospy.Subscriber('number_count', Int16, self.callback)
        self.rate = rate = rospy.Rate(10) # 10hz
    def callback(self, data):
        if self.start == 0:
            self.start = data.data
        else:
            self.start += data.data
    
    def execute(self,data):
        if self.counter < 20:
            self.counter += 1
            print self.start
            self.rate.sleep()
            return 'add'
        else:
            return 'result'

class addNum(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['add'])
    
        
    def execute(self,userdata):
        
        return 'add'

    
def main():
    rospy.init_node('sum_numbers_state_machine')
      
    sm = smach.StateMachine(outcomes = ['finish'])
    
    with sm:
        smach.StateMachine.add('GET', getNum(),
                               transitions ={'add':'ADD',
                                             'result':'finish'})
        smach.StateMachine.add('ADD', addNum(),
                               transitions ={'add':'GET'})
    
    outcome = sm.execute()
    
if __name__ == '__main__':
    main()

