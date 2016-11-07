#!/usr/bin/env python

#-------------------------------
# Written by Yongxi Lu
#-------------------------------

"""Test classificaiton accuracy"""

import _init_paths
from utils.config import cfg, cfg_from_file, cfg_set_path, get_output_dir
from datasets.factory import get_imdb
import argparse
import pprint
import caffe
import sys, os
import json
from evaluation.test import classification_test

import yaml

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description="Test the performance on a dataset.")
    parser.add_argument('--gpu', dest='gpu_id',
                        help='GPU device id to use [None]',
                        default=None, type=int)
    parser.add_argument('--model', dest='model',
                        help='test prototxt',
                        default=None, type=str)
    parser.add_argument('--weights', dest='weights',
                        help='trained caffemodel',
                        default=None, type=str)
    parser.add_argument('--task_name', dest='task_name',
                        help='the name of the task',
                        default='multilabel',type=str)
    parser.add_argument('--cfg', dest='cfg_file',
                        help='optional config file',
                        default=None, type=str)
    parser.add_argument('--imdb', dest='imdb_name',
                        help='datasets to test on',
                        default='celeba_test', type=str)
    parser.add_argument('--mean_file', dest='mean_file',
                        help='the path to the mean file to be used',
                        default=None, type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()

    print('Called with args:')
    print(args)

    if args.cfg_file is not None:
        cfg_from_file(args.cfg_file)

    # use mean file if provided
    if args.mean_file is not None:
        with open(args.mean_file, 'rb') as fid:
            cfg.PIXEL_MEANS = cPickle.load(fid)
            print 'mean values loaded from {}'.format(args.mean_file)

    print('Using config:')
    pprint.pprint(cfg)

    caffe.set_mode_gpu()
    caffe.set_device(args.gpu_id)
    net = caffe.Net(args.model, args.weights, caffe.TEST)
    net.name = os.path.splitext(os.path.basename(args.weights))[0]

    # get imdb
    imdb = get_imdb(args.imdb_name)
    # parse class_id
    classid_name = os.path.splitext(args.weights)[0] + '.clsid'
    with open(classid_name, 'rb') as f:
        class_id = json.loads(f.read())

    classification_test(net, imdb, class_id)