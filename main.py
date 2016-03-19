import os
import numpy as np
import tensorflow as tf

from utils import pp
from models import NVDM, NASM
from reader import TextReader

flags = tf.app.flags
flags.DEFINE_integer("max_iter", 450000, "Maximum of iteration [450000]")
flags.DEFINE_float("learning_rate", 0.001, "Learning rate of for adam [0.001]")
flags.DEFINE_integer("batch_size", 20, "The size of batch images [20]")
flags.DEFINE_integer("embed_dim", 500, "The dimension of word embeddings [500]")
flags.DEFINE_integer("h_dim", 50, "The dimension of latent variable [50]")
flags.DEFINE_string("dataset", "ptb", "The name of dataset [ptb]")
flags.DEFINE_string("model", "nvdm", "The name of model [nvdm, nasm]")
flags.DEFINE_string("checkpoint_dir", "checkpoint", "Directory name to save the checkpoints [checkpoints]")
flags.DEFINE_boolean("forward_only", False, "False for training, True for testing [False]")
FLAGS = flags.FLAGS

MODELS = {
  'nvdm': NVDM,
  'nasm': NASM,
}

def main(_):
  pp.pprint(flags.FLAGS.__flags)

  data_path = "./data/%s" % FLAGS.dataset
  reader = TextReader(data_path, FLAGS.batch_size)

  with tf.Session() as sess:
    m = MODELS[FLAGS.model]
    model = m(sess, reader, dataset=FLAGS.dataset,
              batch_size=FLAGS.batch_size, embed_dim=FLAGS.embed_dim, h_dim=FLAGS.h_dim,
              learning_rate=FLAGS.learning_rate, max_iter=FLAGS.max_iter,
              checkpoint_dir=FLAGS.checkpoint_dir)

    if FLAGS.forward_only:
      model.load(FLAGS.checkpoint_dir)
    else:
      model.train(FLAGS)

    while True:
      text = raw_input(" [*] Enter text to test: ")
      model.sample(5, text)

if __name__ == '__main__':
  tf.app.run()
