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
"""A library describing LexicalMask class and utilities functions."""

from typing import Dict, List

import attr


@attr.s
class LexicalMask(object):
  """A structural representation of a Lexical Mask."""
  language: str = attr.ib()
  langcode: str = attr.ib()
  part_of_speech: str = attr.ib()
  entry_features: List[Dict[str, str]] = attr.ib()
  forms: List[List[str]] = attr.ib()
  name: str = attr.ib()

  def to_shex(self):
    """Returns str of ShEx format converted from an entry."""
    form_shexes = []
    for form in self.forms:
      features = ''.join(
          'wikibase:grammaticalFeature [ wd:%s ];\n    ' % s for s in form)
      form_shex = f"""\
  ontolex:lexicalForm {{
    {features}ontolex:representation [ @{self.langcode} ];
  }};"""
      form_shexes.append(form_shex)
    forms = '\n'.join(form_shexes)

    entry_feature = ''
    if self.entry_features:
      keyed_entry_features = group_features_by_property(self.entry_features)
      for k, values in keyed_entry_features.items():
        entry_feature += '  wdt:%s [ %s ] ;\n' % (k, ' '.join(
            'wd:%s' % v for v in values))

    entry_shex = f"""\
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>

# {self.name}

# SELECT ?focus {{?focus dct:language wd:{self.language};wikibase:lexicalCategory wd:{self.part_of_speech}}}

start = @<{self.langcode}-n>

<{self.langcode}-n> {{
  dct:language [ wd:{self.language} ] ;
  wikibase:lexicalCategory [ wd:{self.part_of_speech} ] ;
  wikibase:lemma [ @{self.langcode} ] ;
{entry_feature}{forms}
}}
"""
    return entry_shex


def group_features_by_property(group_of_features):
  property_to_features: Dict[str, List[str]] = {}
  for features in group_of_features:
    for property_of, feature in features.items():
      property_to_features.setdefault(property_of, []).append(feature)
  return property_to_features
