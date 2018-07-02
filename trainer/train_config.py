import argparse

class TrainConfig:

    # python DCGAN.py --event-file-dir test_1

    class Defaults:
        
        def __init__(self, local):
            self.NUM_EPOCHS = 10
            self.BATCH_SIZE = 128
            self.LOG_FREQ = 1
            self.CHECKPOINT_FREQ = 5

            if local:
                self.DATA_DIR = '/Users/sarahwolf/.keras/datasets/mnist.npz'
                self.SUMMARY_DIR = 'trainer/summary'
                self.CHECKPOINT_DIR = 'MNIST-trained-model'
                self.SAMPLE_DIR = 'trainer/samples'
            else:
                CGP_BUCKET = 'gs://gan-training-207705_bucket2'
                self.DATA_DIR = GCP_BUCKET + '/mnist.npz'
                self.SUMMARY_DIR = GCP_BUCKET + '/output2/summary'
                self.CHECKPOINT_DIR = GCP_BUCKET + '/output2/checkpoints'
                self.SAMPLES_DIR = GCP_BUCKET + '/output2/samples'

    def __init__(self, local=True):
        args = self._add_arguments()
        self._populate_from_args(args, local)

    def _add_arguments(self):
        parser = argparse.ArgumentParser()

        # directories
        parser.add_argument('--data-dir', help='Path to the MNIST data file')
        parser.add_argument('--summary-dir', help='Path to the folder you want the Tensorboard summaries written to')
        parser.add_argument('--checkpoint-dir', help='Path to the folder you want the checkpoints written to')
        parser.add_argument('--sample-dir', help='Path to the folder to write samples to, if in sampling mode. Must also set the --samples flag to a nonzero number for this to do anything.')

        # basic settings
        parser.add_argument('--log-freq', help='Prints the losses and writes Tensorboard summary data every n steps')
        parser.add_argument('--num-epochs', help='number of epochs to train')
        parser.add_argument('--checkpoint-freq', help='Saves partial training progress as checkpoint every n steps')

        # use-cases
        parser.add_argument('--continue-train', help='continue training where we left off')
        parser.add_argument('--sample', help='Sample n images from the generator')

        args = parser.parse_args()
        return args

    def _populate_from_args(self, args, local):
        defaults = self.Defaults(local)

        self.data_dir = args.data_dir or defaults.DATA_DIR
        self.summary_dir = args.summary_dir or defaults.SUMMARY_DIR
        self.checkpoint_dir = args.checkpoint_dir or defaults.CHECKPOINT_DIR
        self.sample_dir = args.sample_dir or defaults.SAMPLE_DIR
        self.log_freq = args.log_freq or defaults.LOG_FREQ
        self.num_epochs = args.num_epochs or defaults.NUM_EPOCHS
        self.checkpoint_freq = args.checkpoint_freq or defaults.CHECKPOINT_FREQ
        self.should_continue = args.continue_train or False
        self.sample = args.sample or 0

