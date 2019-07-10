import argparse

from math import inf

#### Argument parser ####

def setup_argparse():

    parser = argparse.ArgumentParser(description='Cormorant network options')
    # Optimizer options
    parser.add_argument('--num-epoch', type=int, default=255, metavar='N',
                        help='number of epochs to train (default: 511)')
    parser.add_argument('--batch-size', '-bs', type=int, default=25, metavar='N',
                        help='Mini-batch size (default: 25)')
    parser.add_argument('--alpha', type=float, default=0.9, metavar='N',
                        help='Value of alpha to use for exponential moving average of training loss. (default: 0.9)')

    parser.add_argument('--weight-decay', type=float, default=0, metavar='N',
                        help='Set the weight decay used in optimizer (default: 0)')
    parser.add_argument('--cutoff-decay', type=float, default=0, metavar='N',
                        help='Set the weight decay used in optimizer for learnable radial cutoffs (default: 0)')
    parser.add_argument('--lr-init', type=float, default=1e-3, metavar='N',
                        help='Initial learning rate (default: 1e-3)')
    parser.add_argument('--lr-final', type=float, default=1e-5, metavar='N',
                        help='Final (held) learning rate (default: 1e-5)')
    parser.add_argument('--lr-decay', type=int, default=inf, metavar='N',
                        help='Timescale over which to decay the learning rate (default: inf)')
    parser.add_argument('--lr-decay-type', type=str, default='cos', metavar='str',
                        help='Type of learning rate decay. (cos | linear | exponential | pow | restart) (default: cos)')
    parser.add_argument('--lr-minibatch', '--lr-mb', action='store_true',
                        help='Decay learning rate every minibatch instead of epoch.')
    parser.add_argument('--sgd-restart', type=int, default=1, metavar='int',
                        help='Restart SGD optimizer every (lr_decay)^p epochs, where p=sgd_restart.  (default: 1)')

    parser.add_argument('--optim', type=str, default='amsgrad', metavar='str',
                        help='Set optimizer. (SGD, AMSgrad, Adam, RMSprop)')

    parser.add_argument('--predict', dest='predict', action='store_true',
                        help='Save predictions. (default)')
    parser.add_argument('--no-predict', dest='predict', action='store_false',
                        help='Dont save predictions (default)')
    parser.set_defaults(predict=True)

    parser.add_argument('--shuffle', dest='shuffle', action='store_true',
                        help='Shuffle minibatches. (default)')
    parser.add_argument('--no-shuffle', dest='shuffle', action='store_false',
                        help='Dont shuffle minibatches (default)')
    parser.set_defaults(shuffle=True)

    parser.add_argument('--seed', type=int, default=1, metavar='N',
                        help='Set random number seed. Set to -1 to set based upon clock.')

    # Saving and logging options
    parser.add_argument('--save', action='store_true',
                        help='Save checkpoint after each epoch. (default: False)')
    parser.add_argument('--load', action='store_true',
                        help='Load from previous checkpoint. (default: False)')

    parser.add_argument('--skip-test', '--notest', action='store_true',
                        help='Disable initial network testing.')

    ### Arguments for files to save things to
    # Job prefix is used to name checkpoint/best file
    parser.add_argument('--prefix', type=str, default='nosave',
                        help='Prefix to set load, save, and logfile. (default: nosave)')

    # Allow to manually specify file to load
    parser.add_argument('--loadfile', type=str, default='',
                        help='Set checkpoint file to load. Leave empty to auto-generate from prefix. (default: (empty))')
    # Filename to save model checkpoint to
    parser.add_argument('--checkfile', type=str, default='',
                        help='Set checkpoint file to save checkpoints to. Leave empty to auto-generate from prefix. (default: (empty))')
    # Filename to best model checkpoint to
    parser.add_argument('--bestfile', type=str, default='',
                        help='Set checkpoint file to best model to. Leave empty to auto-generate from prefix. (default: (empty))')
    # Filename to save logging information to
    parser.add_argument('--logfile', type=str, default='',
                        help='Duplicate logging.info output to logfile. Set to empty string to generate from prefix. (default: (empty))')
    # Filename to save predictions to
    parser.add_argument('--predictfile', type=str, default='',
                        help='Save predictions to file. Set to empty string to generate from prefix. (default: (empty))')

    # Directory to place logging information
    parser.add_argument('--logdir', type=str, default='log/',
                        help='Directory to place log and savefiles. (default: log/)')
    # Directory to place saved models
    parser.add_argument('--modeldir', type=str, default='model/',
                        help='Directory to place log and savefiles. (default: model/)')
    # Directory to place model predictions
    parser.add_argument('--predictdir', type=str, default='predict/',
                        help='Directory to place log and savefiles. (default: predict/)')
    # Directory to read and save data from
    parser.add_argument('--datadir', type=str, default='data/',
                        help='Directory to look up data from. (default: data/)')

    # Dataset options
    parser.add_argument('--num-train', '--num-samples', dest='num_train', type=int, default=-1, metavar='N',
                        help='Number of samples to train on. Set to -1 to use entire dataset. (default: -1)')
    parser.add_argument('--num-valid', type=int, default=-1, metavar='N',
                        help='Number of validation samples to use. Set to -1 to use entire dataset. (default: -1)')
    parser.add_argument('--num-test', type=int, default=-1, metavar='N',
                        help='Number of test samples to use. Set to -1 to use entire dataset. (default: -1)')

    parser.add_argument('--dataset', type=str, default='qm9',
                        help='Data set. Options: (qm9, md17). Default: qm9.')
    parser.add_argument('--target', type=str, default='',
                        help='Learning target for a dataset (such as qm9) with multiple options.')
    parser.add_argument('--subset', '--molecule', type=str, default='',
                        help='Subset/molecule on data with subsets (such as md17).')

    # Computation options
    parser.add_argument('--cuda', dest='cuda', action='store_true',
                        help='Use CUDA (default)')
    parser.add_argument('--no-cuda', '--cpu', dest='cuda', action='store_false',
                        help='Use CPU')
    parser.set_defaults(cuda=True)

    parser.add_argument('--float', dest='dtype', action='store_const', const='float',
                        help='Use floats.')
    parser.add_argument('--double', dest='dtype', action='store_const', const='double',
                        help='Use doubles.')
    parser.set_defaults(dtype='float')

    # Model options
    parser.add_argument('--num-cg-levels', type=int, default=4, metavar='N',
                        help='Number of CG levels (default: 4)')

    parser.add_argument('--maxl', nargs='*', type=int, default=[3], metavar='N',
                        help='Cutoff in CG operations (default: [3])')
    parser.add_argument('--max-sh', nargs='*', type=int, default=[3], metavar='N',
                        help='Number of spherical harmonic powers to use (default: [3])')
    parser.add_argument('--num-channels', nargs='*', type=int, default=[10], metavar='N',
                        help='Number of channels to allow after mixing (default: [10])')
    parser.add_argument('--level-gain', nargs='*', type=float, default=[10.], metavar='N',
                        help='Gain at each level (default: [10.])')

    parser.add_argument('--charge-power', type=int, default=2, metavar='N',
                        help='Maximum power to take in one-hot (default: 2)')

    parser.add_argument('--hard-cutoff', dest='hard_cut_rad',
                        type=float, default=1.73, nargs='*', metavar='N',
                        help='Radius of HARD cutoff in Angstroms (default: 1.73)')
    parser.add_argument('--soft-cutoff', dest='soft_cut_rad', type=float,
                        default=1.73, nargs='*', metavar='N',
                        help='Radius of SOFT cutoff in Angstroms (default: 1.73)')
    parser.add_argument('--soft-width', dest='soft_cut_width',
                        type=float, default=0.2, nargs='*', metavar='N',
                        help='Width of SOFT cutoff in Angstroms (default: 0.2)')
    parser.add_argument('--cutoff-type', '--cutoff', type=str, default=['soft'], nargs='*', metavar='str',
                        help='Types of cutoffs to include')

    parser.add_argument('--basis-set', '--krange', type=int, default=[3, 3], nargs=2, metavar='N',
                        help='Radial function basis set (m, n) size (default: [3, 3])')

    # TODO: Update(?)
    parser.add_argument('--weight-init', type=str, default='rand', metavar='str',
                        help='Weight initialization function to use (default: rand)')

    parser.add_argument('--input', type=str, default='linear',
                        help='Function to apply to process l0 input (linear | MPNN) default: linear')
    parser.add_argument('--num-mpnn-levels', type=int, default=1,
                        help='Number levels to use in input featurization MPNN. (default: 1)')
    parser.add_argument('--top', '--output', type=str, default='linear',
                        help='Top function to use (linear | PMLP) default: linear')

    parser.add_argument('--gaussian-mask', action='store_true',
                        help='Use gaussian mask instead of sigmoid mask.')

    parser.add_argument('--edge-cat', action='store_true',
                        help='Concatenate the scalars from different \ell in the dot-product-matrix part of the edge network.')

    return parser

# From https://stackoverflow.com/questions/12116685/how-can-i-require-my-python-scripts-argument-to-be-a-float-between-0-0-1-0-usin
class Range(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __eq__(self, other):
        return self.start <= other <= self.end