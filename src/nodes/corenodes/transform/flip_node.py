# ----------------------------------------------------------------------------
# Gimel Studio Copyright 2019-2021 by Noah Rahm and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------

try:
    import OpenImageIO as oiio
except ImportError:
    print("""OpenImageIO is required! Get the python wheel for Windows at:
     https://www.lfd.uci.edu/~gohlke/pythonlibs/#openimageio""")

from gimelstudio import api


class FlipNode(api.Node):
    def __init__(self, nodegraph, _id):
        api.Node.__init__(self, nodegraph, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Flip",
            "author": "Gimel Studio",
            "version": (0, 5, 0),
            "category": "TRANSFORM",
            "description": "Flips the orientation of the image.",
        }
        return meta_info

    def NodeInitProps(self):
        self.direction = api.ChoiceProp(
            idname="direction",
            default="Vertically",
            choices=["Vertically", "Horizontally", "Diagonally"],
            label="Orientation"
        )
        self.NodeAddProp(self.direction)

    def NodeInitParams(self):
        image = api.RenderImageParam("image", "Image")

        self.NodeAddParam(image)

    def NodeEvaluation(self, eval_info):
        flip_direction = self.EvalProperty(eval_info, "direction")
        image1 = self.EvalParameter(eval_info, "image")

        render_image = api.RenderImage()
        img = image1.Image("oiio")

        if flip_direction == "Vertically":
            output_img = oiio.ImageBufAlgo.flip(img)
        elif flip_direction == "Horizontally":
            output_img = oiio.ImageBufAlgo.flop(img)
        elif flip_direction == "Diagonally":
            output_img = oiio.ImageBufAlgo.transpose(img)

        render_image.SetAsImage(output_img)
        self.NodeUpdateThumb(render_image)
        return render_image


api.RegisterNode(FlipNode, "corenode_flip")
