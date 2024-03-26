import hou
from PySide2 import QtWidgets
import os
import shutil
from glob import glob



class QuixelImporter(QtWidgets.QWidget):

        def __init__(self):

                super().__init__()

                self.setWindowTitle("Import Quixel Scan")
                self.setGeometry(500,300,700,500)

                main_layout = QtWidgets.QVBoxLayout()
                self.setLayout(main_layout)


                #---------------------Asset Name---------------------------------------------

                name_layout = QtWidgets.QHBoxLayout()
                main_layout.addLayout(name_layout)

                name_label = QtWidgets.QLabel("Asset Name")
                name_layout.addWidget(name_label)

                self.asset_name = QtWidgets.QLineEdit()
                name_layout.addWidget(self.asset_name)

                clear_button = QtWidgets.QPushButton("Clear Inputs")
                name_layout.addWidget(clear_button)
                clear_button.clicked.connect(self.clear)


                #---------------------Autofill-----------------------------------------------

                import_button = QtWidgets.QPushButton("Autofill")
                main_layout.addWidget(import_button)
                import_button.clicked.connect(self.get_quixel_asset)


                #-----------------------Base Color Input--------------------------------------

                base_color_input_layout = QtWidgets.QHBoxLayout()
                main_layout.addLayout(base_color_input_layout)

                base_color_path_label = QtWidgets.QLabel("Base Color")
                base_color_input_layout.addWidget(base_color_path_label)

                self.base_color_path = QtWidgets.QLineEdit()
                base_color_input_layout.addWidget(self.base_color_path)

                set_base_color_button = QtWidgets.QPushButton("Repath")
                base_color_input_layout.addWidget(set_base_color_button)
                set_base_color_button.clicked.connect(lambda: self.change_path(self.base_color_path))


                #-----------------------Roughness Input--------------------------------------

                roughness_input_layout = QtWidgets.QHBoxLayout()
                main_layout.addLayout(roughness_input_layout)

                roughness_path_label = QtWidgets.QLabel("Roughness")
                roughness_input_layout.addWidget(roughness_path_label)

                self.roughness_path = QtWidgets.QLineEdit()
                roughness_input_layout.addWidget(self.roughness_path)

                set_roughness_button = QtWidgets.QPushButton("Repath")
                roughness_input_layout.addWidget(set_roughness_button)
                set_roughness_button.clicked.connect(lambda: self.change_path(self.roughness_path))



                #-----------------------Metalness Input--------------------------------------
                metalness_input_layout = QtWidgets.QHBoxLayout()
                main_layout.addLayout(metalness_input_layout)

                metalness_path_label = QtWidgets.QLabel("Metalness")
                metalness_input_layout.addWidget(metalness_path_label)

                self.metalness_path = QtWidgets.QLineEdit()
                metalness_input_layout.addWidget(self.metalness_path)

                set_metalness_button = QtWidgets.QPushButton("Repath")
                metalness_input_layout.addWidget(set_metalness_button)
                set_metalness_button.clicked.connect(lambda: self.change_path(self.metalness_path))
           

                #-----------------------Normal Input--------------------------------------
                normal_input_layout = QtWidgets.QHBoxLayout()
                main_layout.addLayout(normal_input_layout)

                normal_path_label = QtWidgets.QLabel("Normal")
                normal_input_layout.addWidget(normal_path_label)

                self.normal_path = QtWidgets.QLineEdit()
                normal_input_layout.addWidget(self.normal_path)

                set_normal_button = QtWidgets.QPushButton("Repath")
                normal_input_layout.addWidget(set_normal_button)
                set_normal_button.clicked.connect(lambda: self.change_path(self.normal_path))


                #-----------------------Displacement Input--------------------------------------
                displacement_input_layout = QtWidgets.QHBoxLayout()
                main_layout.addLayout(displacement_input_layout)

                displacement_path_label = QtWidgets.QLabel("Displacement")
                displacement_input_layout.addWidget(displacement_path_label)

                self.displacement_path = QtWidgets.QLineEdit()
                displacement_input_layout.addWidget(self.displacement_path)

                set_displacement_button = QtWidgets.QPushButton("Repath")
                displacement_input_layout.addWidget(set_displacement_button)
                set_displacement_button.clicked.connect(lambda: self.change_path(self.displacement_path))


               #-----------------------Opacity Input--------------------------------------
                opacity_input_layout = QtWidgets.QHBoxLayout()
                main_layout.addLayout(opacity_input_layout)

                opacity_path_label = QtWidgets.QLabel("Opacity")
                opacity_input_layout.addWidget(opacity_path_label)

                self.opacity_path = QtWidgets.QLineEdit()
                opacity_input_layout.addWidget(self.opacity_path)

                set_opacity_button = QtWidgets.QPushButton("Repath")
                opacity_input_layout.addWidget(set_opacity_button)
                set_opacity_button.clicked.connect(lambda: self.change_path(self.opacity_path))


                shader_options_layout = QtWidgets.QHBoxLayout()
                main_layout.addLayout(shader_options_layout)

                build_mats_button = QtWidgets.QPushButton("Build Material Network")
                shader_options_layout.addWidget(build_mats_button)
                build_mats_button.clicked.connect(self.build_materials)

                self.shader_options = QtWidgets.QComboBox()
                self.shader_options.addItem("Arnold")
                self.shader_options.addItem("Redshift")
                shader_options_layout.addWidget(self.shader_options)

                #-------------------------Geometry Input---------------------------------
                geo_input_layout = QtWidgets.QHBoxLayout()
                main_layout.addLayout(geo_input_layout)

                geo_path_label = QtWidgets.QLabel("Geometry")
                geo_input_layout.addWidget(geo_path_label)

                self.geo_path = QtWidgets.QLineEdit()
                geo_input_layout.addWidget(self.geo_path)

                set_geo_button = QtWidgets.QPushButton("Repath")
                geo_input_layout.addWidget(set_geo_button)
                set_geo_button.clicked.connect(lambda: self.change_path(self.geo_path))


                build_geo_button = QtWidgets.QPushButton("Build Geometry Network")
                main_layout.addWidget(build_geo_button)
                build_geo_button.clicked.connect(self.build_asset)


        def build_arnold_shader(self, material_name):

                context = hou.node("/mat")
                material_network = context.createNode("arnold_materialbuilder", material_name)

                surface_shader = material_network.createNode("arnold::standard_surface","standard_surface")
                material_output = hou.node(material_network.path() + "/OUT_material")

                material_output.setNamedInput("surface", surface_shader, "shader")


                if "base_color" in self.texture_pathing:
                        base_color_texture = material_network.createNode("arnold::image", "base_color_texture")
                        base_color_texture.parm("filename").set(self.texture_pathing["base_color"])
                        surface_shader.setNamedInput("base_color", base_color_texture, "rgba")


                if "roughness" in self.texture_pathing:
                        roughness_texture = material_network.createNode("arnold::image", "roughness_texture")
                        roughness_texture.parm("color_family").set("Utility")
                        roughness_texture.parm("color_space").set("Raw")
                        roughness_texture.parm("filename").set(self.texture_pathing["roughness"])
                        roughness_correct = material_network.createNode("arnold::color_correct", "rougness_correction")
                        roughness_correct.parm("alpha_is_luminance").set(True)
                        roughness_correct.setNamedInput("input", roughness_texture, "rgba")
                        surface_shader.setNamedInput("specular_roughness", roughness_correct, "rgba")

                if "normal" in self.texture_pathing:
                        normal_texture = material_network.createNode("arnold::image", "normal_texture")
                        normal_texture.parm("color_family").set("Utility")
                        normal_texture.parm("color_space").set("Raw")
                        normal_texture.parm("filename").set(self.texture_pathing["normal"])
                        normal_mapping = material_network.createNode("arnold::normal_map", "normal_map")
                        normal_mapping.setNamedInput("input", normal_texture, "rgba")
                        surface_shader.setNamedInput("normal", normal_mapping, "vector")

                if "displacement" in self.texture_pathing:
                        displacement_texture = material_network.createNode("arnold::image", "displacement_texture")
                        displacement_texture.parm("color_family").set("Utility")
                        displacement_texture.parm("color_space").set("Raw")
                        displacement_texture.parm("filename").set(self.texture_pathing["displacement"])
                        displacement_correct = material_network.createNode("arnold::color_correct", "displacement_correction")
                        displacement_correct.parm("alpha_is_luminance").set(True)
                        displacement_correct.setNamedInput("input", displacement_texture, "rgba")
                        material_output.setNamedInput("displacement", displacement_correct, "rgba")

                if "metalness" in self.texture_pathing:
                        metalness_texture = material_network.createNode("arnold::image", "metalness_texture")
                        metalness_texture.parm("color_family").set("Utility")
                        metalness_texture.parm("color_space").set("Raw")
                        metalness_texture.parm("filename").set(self.texture_pathing["metalness"])
                        metalness_correct = material_network.createNode("arnold::color_correct", "metalness_correction")
                        metalness_correct.parm("alpha_is_luminance").set(True)
                        metalness_correct.setNamedInput("input", metalness_texture, "rgba")
                        surface_shader.setNamedInput("metalness", metalness_correct, "rgba")

                if "opacity" in self.texture_pathing:
                        opacity_texture = material_network.createNode("arnold::image", "opacity_texture")
                        opacity_texture.parm("color_family").set("Utility")
                        opacity_texture.parm("color_space").set("Raw")
                        opacity_texture.parm("filename").set(self.texture_pathing["opacity"])
                        opacity_correct = material_network.createNode("arnold::color_correct", "opacity_correction")
                        opacity_correct.parm("alpha_is_luminance").set(True)
                        opacity_correct.setNamedInput("input", opacity_texture, "rgba")
                        surface_shader.setNamedInput("opacity", opacity_correct, "rgba")

                material_network.layoutChildren()


        def build_redshift_shader(self, material_name):

                context = hou.node("/mat")
                material_network = context.createNode("redshift_vopnet", material_name)

                surface_shader = hou.node(material_network.path()+ "/StandardMaterial1")
                material_output = hou.node(material_network.path() + "/redshift_material1")

                if "base_color" in self.texture_pathing:
                        base_color_texture = material_network.createNode("redshift::TextureSampler", "base_color_texture")
                        base_color_texture.parm("tex0").set(self.texture_pathing["base_color"])
                        surface_shader.setNamedInput("base_color", base_color_texture, "outColor")


                if "roughness" in self.texture_pathing:
                        roughness_texture = material_network.createNode("redshift::TextureSampler", "roughness_texture")
                        roughness_texture.parm("tex0_colorSpace").set("Raw")
                        roughness_texture.parm("tex0").set(self.texture_pathing["roughness"])
                        roughness_texture.parm("alpha_is_luminance").set(True)
                        surface_shader.setNamedInput("refl_roughness", roughness_texture, "outColor")

                if "normal" in self.texture_pathing:
                        normal_texture = material_network.createNode("redshift::NormalMap", "normal_texture")
                        normal_texture.parm("tex0").set(self.texture_pathing["normal"])
                        surface_shader.setNamedInput("bump_input", normal_texture, "outDisplacementVector")

                if "displacement" in self.texture_pathing:
                        displacement_texture = material_network.createNode("redshift::TextureSampler", "displacement_texture")
                        displacement_texture.parm("tex0_colorSpace").set("Raw")
                        displacement_texture.parm("tex0").set(self.texture_pathing["displacement"])
                        displacement_texture.parm("alpha_is_luminance").set(True)
                        displacement_map = material_network.createNode("redshift::Displacement", "displacement_map")
                        displacement_map.setNamedInput("texMap", displacement_texture, "outColor")
                        material_output.setNamedInput("Displacement", displacement_map, "out")

                if "metalness" in self.texture_pathing:
                        metalness_texture = material_network.createNode("redshift::TextureSampler", "metalness_texture")
                        metalness_texture.parm("tex0_colorSpace").set("Raw")
                        metalness_texture.parm("tex0").set(self.texture_pathing["metalness"])
                        metalness_texture.parm("alpha_is_luminance").set(True)
                        surface_shader.setNamedInput("metalness", metalness_texture, "outColor")

                if "opacity" in self.texture_pathing:
                        opacity_texture = material_network.createNode("redshift::TextureSampler", "opacity_texture")
                        opacity_texture.parm("tex0_colorSpace").set("Raw")
                        opacity_texture.parm("tex0").set(self.texture_pathing["opacity"])
                        opacity_texture.parm("alpha_is_luminance").set(True)
                        surface_shader.setNamedInput("opacity_color", opacity_texture, "outColor")

                material_network.layoutChildren()



        def import_geo(self, geo_name):
                print("runb")
                context = hou.node("/obj")
                asset_network = context.createNode("geo", geo_name)
                file_import = asset_network.createNode("file", geo_name + "_import")
                file_import.parm("file").set(self.geo_pathing)
                scale = asset_network.createNode("xform", "scale_correction")
                scale.parm("scale").set(0.01)
                scale.setInput(0,file_import)
                material = asset_network.createNode("material","scan_material")
                material.parm("shop_materialpath1").set("/mat/"+self.asset_name.text()+"_mat")
                material.setInput(0,scale)
                out = asset_network.createNode("null", "OUT_"+geo_name)
                out.setInput(0,material)

                asset_network.layoutChildren()


        def build_materials(self):

                if self.asset_name.text() != "":
                        if " " in self.asset_name.text():
                                whitespace_name_error = QtWidgets.QMessageBox.critical(self, "Error", "Whitespace in asset name")
                        else:
                                self.transfer_tex_files()

                                if self.shader_options.currentText() == "Arnold":

                                        self.build_arnold_shader(self.asset_name.text()+"_mat")

                                if self.shader_options.currentText() == "Redshift":

                                        self.build_redshift_shader(self.asset_name.text()+"_mat")
                else:
                        no_name_error = QtWidgets.QMessageBox.critical(self,"Error", "Asset has no name")

        def build_asset(self):


                if self.asset_name.text() != "":
                        if " " in self.asset_name.text():
                                whitespace_name_error = QtWidgets.QMessageBox.critical(self, "Error", "Whitespace in asset name")
                        else:
                                self.transfer_geo_files()
                                print("runa")
                                self.import_geo(self.asset_name.text())

                else:
                        no_name_error = QtWidgets.QMessageBox.critical(self,"Error", "Asset has no name")


        def get_quixel_asset(self):

                path = QtWidgets.QFileDialog.getExistingDirectory(self,caption = "Select Asset Directory",
                                                                directory = os.path.expanduser("~"))
                geo_search = path + "/**/*.fbx"
                geo_files = glob(geo_search, recursive=True)
                if len(geo_files)>0: self.geo_path.setText(geo_files[0])

                base_color_search = path + "/**/*Albedo*"
                base_color_files = glob(base_color_search, recursive=True)
                if len(base_color_files)>0: self.base_color_path.setText(base_color_files[0])

                roughness_search = path + "/**/*Roughness*"
                roughness_files = glob(roughness_search, recursive=True)
                if len(roughness_files)>0: self.roughness_path.setText(roughness_files[0])

                metalness_search = path + "/**/*Metalness*"
                metalness_files = glob(metalness_search, recursive=True)
                if len(metalness_files)>0: self.metalness_path.setText(metalness_files[0])

                normal_search = path + "/**/*Normal*"
                normal_files = glob(normal_search, recursive=True)
                if len(normal_files)>0: self.normal_path.setText(normal_files[0])

                displacement_search = path + "/**/*Displacement*"
                displacement_files = glob(displacement_search, recursive=True)
                if len(displacement_files)>0: self.displacement_path.setText(displacement_files[0])

                opacity_search = path + "/**/*Opacity*"
                opacity_files = glob(opacity_search, recursive=True)
                if len(opacity_files)>0: self.opacity_path.setText(opacity_files[0])


        def change_path(self, path_input):

                tex_path = QtWidgets.QFileDialog.getOpenFileName(self, caption = "Select Texture File",
                                                                directory = os.path.expanduser("~"))[0]
                path_input.setText(tex_path)


        def transfer_tex_files(self):


                self.texture_pathing = {}
                hip_dir = os.path.dirname(hou.hipFile.path())
                hip_tex_dir = os.path.join(hip_dir,"tex")
                asset_tex_dir = os.path.join(hip_tex_dir, self.asset_name.text())
                if os.path.isdir(hip_tex_dir)is True and os.path.isdir(asset_tex_dir) is False:
                        os.mkdir(asset_tex_dir)

                if self.roughness_path.text() != "" and os.path.exists(self.roughness_path.text()) is True:

                        extension = os.path.splitext(self.roughness_path.text())[1]
                        roughness_map = self.asset_name.text() + "_roughness"+ extension
                        roughness_map_path = os.path.join(asset_tex_dir, roughness_map)

                        if os.path.exists(roughness_map_path) is False:
                                shutil.copy(self.roughness_path.text(), roughness_map_path)

                        self.texture_pathing["roughness"] = "$HIP/" + os.path.relpath(roughness_map_path, hip_dir)


                if self.base_color_path.text() != "" and os.path.exists(self.base_color_path.text()) is True:

                        extension = os.path.splitext(self.base_color_path.text())[1]
                        base_color_map = self.asset_name.text() + "_color"+ extension
                        base_color_map_path = os.path.join(asset_tex_dir, base_color_map)

                        if os.path.exists(base_color_map_path) is False:
                                shutil.copy(self.base_color_path.text(), base_color_map_path)

                        self.texture_pathing["base_color"] = "$HIP/" + os.path.relpath(base_color_map_path, hip_dir)


                if self.metalness_path.text() != "" and os.path.exists(self.metalness_path.text()) is True:

                        extension = os.path.splitext(self.metalness_path.text())[1]
                        metalness_map = self.asset_name.text() + "_metalness"+ extension
                        metalness_map_path = os.path.join(asset_tex_dir, metalness_map)

                        if os.path.exists(metalness_map_path) is False:
                                shutil.copy(self.metalness_path.text(), metalness_map_path)

                        self.texture_pathing["metalness"] = "$HIP/" + os.path.relpath(metalness_map_path, hip_dir)


                if self.normal_path.text() != "" and os.path.exists(self.normal_path.text()) is True:

                        extension = os.path.splitext(self.normal_path.text())[1]
                        normal_map = self.asset_name.text() + "_normal"+ extension
                        normal_map_path = os.path.join(asset_tex_dir, normal_map)

                        if os.path.exists(normal_map_path) is False:
                                shutil.copy(self.normal_path.text(), normal_map_path)

                        self.texture_pathing["normal"] = "$HIP/" + os.path.relpath(normal_map_path, hip_dir)


                if self.displacement_path.text() != "" and os.path.exists(self.displacement_path.text()) is True:

                        extension = os.path.splitext(self.displacement_path.text())[1]
                        displacement_map = self.asset_name.text() + "_displacement"+ extension
                        displacement_map_path = os.path.join(asset_tex_dir, displacement_map)

                        if os.path.exists(displacement_map_path) is False:
                                shutil.copy(self.displacement_path.text(), displacement_map_path)

                        self.texture_pathing["displacement"] = "$HIP/" + os.path.relpath(displacement_map_path, hip_dir)


                if self.opacity_path.text() != "" and os.path.exists(self.opacity_path.text()) is True:

                        extension = os.path.splitext(self.opacity_path.text())[1]
                        opacity_map = self.asset_name.text() + "_opacity"+ extension
                        opacity_map_path = os.path.join(asset_tex_dir, opacity_map)

                        if os.path.exists(opacity_map_path) is False:
                                shutil.copy(self.opacity_path.text(), opacity_map_path)

                        self.texture_pathing["opacity"] = "$HIP/" + os.path.relpath(opacity_map_path, hip_dir)

        def transfer_geo_files(self):

                hip_dir = os.path.dirname(hou.hipFile.path())
                hip_geo_dir = os.path.join(hip_dir, "geo")
                if self.geo_path.text() != "" and os.path.exists(self.geo_path.text()) is True:

                        extension = os.path.splitext(self.geo_path.text())[1]
                        asset_geo = self.asset_name.text() +"_asset"+ extension
                        asset_geo_path = os.path.join(hip_geo_dir, asset_geo)

                        if os.path.exists(asset_geo_path) is False:
                                shutil.copy(self.geo_path.text(), asset_geo_path)
                        self.geo_pathing = "$HIP/" + os.path.relpath(asset_geo_path, hip_dir)


        def clear(self):

                self.asset_name.clear()
                self.base_color_path.clear()
                self.roughness_path.clear()
                self.metalness_path.clear()
                self.normal_path.clear()
                self.displacement_path.clear()
                self.opacity_path.clear()
                self.geo_path.clear()
                        

