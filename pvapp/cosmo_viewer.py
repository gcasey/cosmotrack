################################################################################
#
# Copyright 2013 Kitware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
################################################################################

# import to process args
import sys
import os
import math
import json

import argparse

# import annotations
from autobahn.wamp import exportRpc

# import paraview modules.
from paraview import simple, web, servermanager, web_helper, paraviewweb_wamp, paraviewweb_protocols

# Setup global variables
timesteps = []
currentTimeIndex = 0
view = None
authKey = None

def initView(width, height):
    global view
    view = simple.GetRenderView()
    simple.Render()
    view.ViewSize = [width, height]
    view.Background = [0.0, 0.0, 0.0]
    view.OrientationAxesLabelColor = [0, 0, 0]

# This class defines the exposed RPC methods for the midas application
class CosmoApp(paraviewweb_wamp.ServerProtocol):
    def initialize(self):
        global authKey

        # Bring used components
        self.registerParaViewWebProtocol(paraviewweb_protocols.ParaViewWebMouseHandler())
        self.registerParaViewWebProtocol(paraviewweb_protocols.ParaViewWebViewPort())
        self.registerParaViewWebProtocol(paraviewweb_protocols.ParaViewWebViewPortImageDelivery())
        self.registerParaViewWebProtocol(paraviewweb_protocols.ParaViewWebViewPortGeometryDelivery())

        # Update authentication key to use
        self.updateSecret(authKey)
        self.scalarBar = None

    @exportRpc("loadData")
    def loadData(self, filename):
        """
        Loads the data specified by filename, and returns
        its fileid and a list of available information arrays
        with type information.
        """
        global view

        try:
            simple.Delete()
        except:
            pass
        if(self.scalarBar is not None):
            view.Representations.remove(self.scalarBar)

        self.src = simple.OpenDataFile(filename)
        self.rep = simple.Show()
        simple.Render()
        simple.ResetCamera()
        fileid = self.src.GetGlobalIDAsString()

        (pdi, cdi) = (self.src.GetPointDataInformation(),
                      self.src.GetCellDataInformation())
        infoArrays = []
        for idx in range(0, pdi.GetNumberOfArrays()):
            infoArray = pdi.GetArray(idx)
            infoArrays.append({
                'type' : 'Point',
                'name' : infoArray.Name,
                'range' : infoArray.GetRange()
                })
        for idx in range(0, cdi.GetNumberOfArrays()):
            infoArray = cdi.GetArray(idx)
            infoArrays.append({
                'type' : 'Cell',
                'name' : infoArray.Name,
                'range' : infoArray.GetRange()
                })

        return {'fileId' : fileid,
                'infoArrays' : infoArrays}

    @exportRpc("colorBy")
    def colorBy(self, colorArrayName, min, max):
        global view
        colorArrayName = colorArrayName.encode('ascii', 'ignore')
        lut = simple.MakeBlueToRedLT(min, max)

        if(self.scalarBar is not None):
            view.Representations.remove(self.scalarBar)

        self.scalarBar = simple.CreateScalarBar(Title=colorArrayName, LabelFontSize=12,
            Enabled=1, LookupTable=lut, TitleFontSize=12)


        view.Representations.append(self.scalarBar)

        self.rep.ColorArrayName = colorArrayName
        self.rep.LookupTable = lut

        simple.Render()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Midas+ParaViewWeb application")
    web.add_arguments(parser)
    parser.add_argument("--width", default=400,
        help="width of the render window", dest="width")
    parser.add_argument("--height", default=400,
        help="height of the render window", dest="height")
    args = parser.parse_args()

    authKey = args.authKey
    width = args.width
    height = args.height

    initView(width, height)
    web.start_webserver(options=args, protocol=CosmoApp)
