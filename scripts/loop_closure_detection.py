#!/usr/bin/env python3

# Loop Closure Detection service
# Multiple implementations of loop closure detection for benchmarking

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

from cslam_loop_detection.srv import DetectLoopClosure
from external_loop_closure_detection.netvlad_loop_closure_detection import NetVLADLoopClosureDetection
from external_loop_closure_detection.vit_loop_closure_detection import ViTLoopClosureDetection

class LoopClosureDetection(Node):

    def __init__(self):
        super().__init__('loop_closure_detection')

        self.declare_parameters(
            namespace='',
            parameters=[
                ('threshold', None),
                ('min_inbetween_keyframes', None),
                ('nb_best_matches', None),
                ('technique', None),
                ('pca', None),
                ('resume', None),
                ('checkpoint', None),
                ('crop_size', None)
            ]
        )
        params = {}
        params['threshold'] = self.get_parameter('threshold').value
        params['min_inbetween_keyframes'] = self.get_parameter('min_inbetween_keyframes').value
        params['nb_best_matches'] = self.get_parameter('nb_best_matches').value
        params['technique'] = self.get_parameter('technique').value
        if params['technique'].lower() == 'netvlad':
            params['pca'] = self.get_parameter('pca').value
        params['resume'] = self.get_parameter('resume').value
        params['checkpoint'] = self.get_parameter('checkpoint').value
        params['crop_size'] = self.get_parameter('crop_size').value

        if params['technique'].lower() == 'netvlad':
            self.lcd = NetVLADLoopClosureDetection(params, self)
        elif params['technique'].lower() == 'vit':
            self.lcd = ViTLoopClosureDetection(params, self)
        else:
            self.get_logger().err('ERROR: Unknown technique')

        self.srv = self.create_service(DetectLoopClosure, 'detect_loop_closure', self.service)

    def get_node(self):
        return self

    def service(self, req, res):
        # Call all methods we want to test
        res = self.lcd.detect_loop_closure_service(req, res)
        return res

if __name__ == '__main__':
    
    rclpy.init(args=None)
    lcd = LoopClosureDetection()
    rclpy.spin(lcd)
    rclpy.shutdown()
