# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Lint as: python3
"""Converts LexicalMask represented in JSON to multiple ShEx in a file."""

import json

from absl import app
from absl import flags

import wikidata

flags.DEFINE_string('lexical_mask', None, 'File path to lexical mask JSON.')
flags.DEFINE_string('output_shex', None, 'File path to output ShEx format.')
FLAGS = flags.FLAGS


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  with open(FLAGS.lexical_mask, mode='r') as mask_file:
    json_masks = json.loads(mask_file.read())
  masks = [wikidata.LexicalMask(**j) for j in json_masks]

  shex = [mask.to_shex() for mask in masks]

  with open(FLAGS.output_shex, mode='w') as output_shex:
    output_shex.write('\n\n#############\n'.join(shex))


if __name__ == '__main__':
  app.run(main)
