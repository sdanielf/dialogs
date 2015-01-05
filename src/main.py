#!/usr/bin/env python3

import sys
import json
from gi.repository import Gtk


class Text:
    def build(self, info):
        self.id = info['id']
        self.widget = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label()
        label.set_text(info['label'])
        label.show()
        self.entry = Gtk.Entry()
        self.entry.show()
        self.widget.pack_start(label, False, False, 0)
        self.widget.pack_start(self.entry, True, True, 0)
        self.widget.show()

    def value(self):
        return self.entry.get_text()


class Dialog:
    def build(self, info):
        self.children = []
        self.widget = Gtk.Dialog()
        self.widget.set_title(info['title'])
        box = self.widget.get_content_area()
        for label, response in info['buttons']:
            self.widget.add_button(label, response)
        for child_info in info['content']:
            element = build_element(child_info)
            self.children.append(element)
            box.pack_start(element.widget, True, True, 0)

    def value(self):
        resp = self.widget.run()
        output = {'response': resp}
        for child in self.children:
            output[child.id] = child.value()
        return output


types = {'dialog': Dialog, 'text': Text}


def build_element(info):
    element = types[info['type']]()
    element.build(info)
    return element

file_path = sys.argv[1]
stream = open(file_path, 'r')
content = json.load(stream)
stream.close()

output = {}

for name in content:
    element = build_element(content[name])
    output[name] = element.value()

stream = open(sys.argv[2], 'w')
json.dump(output, stream)
stream.close()
# Gtk.main()
