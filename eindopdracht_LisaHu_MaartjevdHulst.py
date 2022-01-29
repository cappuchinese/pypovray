#!/usr/bin/python3

"""
This program renders an animation with the use of the PyPovRay library.
The animation with visualize the mechanism of the second step in the citric acid cycle:
    citrate to isocitrate in the enzyme aconitase.
"""

__author__ = "Lisa Hu & Maartje van der Hulst"
__date__ = 2021.12
__version__ = 1.0

# IMPORTS
import sys
from math import pi
from pypovray import pypovray, pdb, SETTINGS, models
from vapory import Scene, Texture, Pigment, Finish, Sphere, LightSource, Camera, Background
import datetime


# OBJECTS
class PovRayObjects:
    """
    Module to make the objects used in PovRay movie
    """
    def __init__(self):
        self.citrate, self.isocitrate = self.get_molecules()
        self.enzyme = self.make_enzyme()

    @staticmethod
    def make_enzyme():
        """
        Enzyme object
        """
        # Style model for the spheres
        sphere_style = Texture(Pigment('color', [1, 0.7, 0.75], 'filter', 0),
                               Finish('phong', 0.2, 'reflection', 0.3))
        # Spheres
        sphere1 = Sphere([30, -1, 0], 5, sphere_style)  # Bottom left
        sphere2 = Sphere([35, -1, 0], 5, sphere_style)  # Bottom right
        sphere3 = Sphere([30, 4, 0], 5, sphere_style)  # Top left
        sphere4 = Sphere([35, 4, 0], 5, sphere_style)  # Top right

        return [sphere1, sphere2, sphere3, sphere4]

    @staticmethod
    def get_molecules():
        """
        Chemical components
        """
        citrate = pdb.PDBMolecule(f"{SETTINGS.AppLocation}pdb/citrate_new.pdb",
                                  center=True, offset=[0, 0, 0])
        isocitrate = pdb.PDBMolecule(f"{SETTINGS.AppLocation}pdb/isocitrate_new.pdb",
                                     center=True, offset=[0, 0, 0])

        return citrate, isocitrate


# FUNCTIONS
class PovRayFunctions:
    """
    Module for functions used in PovRay movie
    """
    def __init__(self, tf_end):
        """
        Initializing function
        :param tf_end: List of last frames per scene
        """
        self.tf_end = tf_end

    def get_timesframes(self):
        """
        Create the lists of start frames and duration frames
        """
        tf_start = []
        start_point = 0
        for i in range(len(self.tf_end)):
            # i = [0, 1, 2...]
            tf_start.append(start_point)
            # start_point = [120, 240, 420...]
            start_point = self.tf_end[i]
            # tf_start = [0, 120, 240, 420...]

        # i = index of the start list
        # Subtracting the end time with start time results in duration time
        tf_dur = [self.tf_end[i] - tf_start[i] for i in range(len(tf_start))]

        return tf_start, tf_dur

    @staticmethod
    def get_distance(step, duration, distance, start_time=0):
        """
        Get distances per frame
        :param step: Step in the scene
        :param duration: Duration of the scene in seconds
        :param distance: [x, y, z] vector
        :param start_time: Start of the movement in the scene, default 0
        """
        total_frames = SETTINGS.RenderFPS * duration
        first_frame = (step + 1) - SETTINGS.RenderFPS * start_time
        distances = [x / total_frames * first_frame for x in distance]

        return distances

    @staticmethod
    def rotate_molecule(rotation, molecule, duration, step):
        """
        Function to let the molecule rotate
        :param rotation: Amount of rotation in radials
        :param molecule: Molecule to rotate
        :param duration: Duration of the rotation in frames
        :param step: Step in the rotation
        """
        rads = (rotation * pi / duration) * step
        molecule.rotate([1, 1, 0], rads)


# SCENES
class PovRayScenes:
    """
    Scenes used for the povray movie
    """

    def __init__(self, pr_objs, pr_funcs, tf_start, tf_dur, tf_end):
        """
        Initializing function
        :param pr_objs: PovRayObjects class
        :param pr_funcs: PovRayFunctions class
        :param tf_start: List of frames when the scenes start
        :param tf_dur: List of amounts of frames per scene
        :param tf_end: List of last frame per scene
        """
        self.probj = pr_objs
        self.prfunc = pr_funcs
        self.start = tf_start
        self.dur = tf_dur
        self.end = tf_end

    def s1_citrate_rotation(self, step):
        """
        First scene: Rotating citrate for visualization
        """
        # Create camera and light source
        camera = Camera('location', [0, 0, -30], 'look_at', [0, 0, 0])
        lighting = LightSource([0, 0, -20], 'color', [1, 1, 1])
        # Get the citrate molecule
        citrate = self.probj.citrate
        # Let citrate rotate
        self.prfunc.rotate_molecule(2, citrate, self.dur[0] * 30, step)
        # List of objects to render
        objects = citrate.povray_molecule + [lighting]

        return Scene(camera, objects=objects)

    def s2_moving(self, step):
        """
        Second scene: Moving citrate into the enzyme
        """
        # Create light source
        lighting = LightSource([0, 0, -20], 'color', [1, 1, 1])

        # Get the position of the camera
        position = self.prfunc.get_distance(step, self.dur[1], [31, 0, 0])
        # Set the z position backwards
        position[2] = -30
        # Get the position of citrate and the camera look position
        looking = self.prfunc.get_distance(step, self.dur[1], [31, 0, 0])
        camera = Camera('location', position, 'look_at', looking)

        # Get citrate and enzyme
        enzyme = self.probj.enzyme
        citrate = self.probj.citrate
        citrate.move_offset(looking)

        # List of objects to render
        objects = citrate.povray_molecule + enzyme + [lighting]

        return Scene(camera, objects=objects)

    def s3_fading_in(self, step):
        """
        Third scene: Camera moves 'into' the enzyme, light fades
        :return:
        """
        # Get the camera location
        position = self.prfunc.get_distance(step, self.dur[2], [0, 0, 25])
        position[0] = 32
        position[2] -= 30
        camera = Camera('location', position, 'look_at', [30, 0, 0])
        # Let the light fade out
        intensity = self.prfunc.get_distance(step, self.dur[2], [-1, -1, -1])
        # Outcome of function above is negative -> set positive
        intensity[:] = [number + 1 for number in intensity]
        # Light source that fades out
        lighting = LightSource([0, 0, -20], 'color', intensity)

        # Get enzyme object
        enzyme = self.probj.enzyme
        # List of objects to render
        objects = enzyme + [lighting]

        return Scene(camera, objects=objects)

    def s4_switching(self, step):
        """
        Fourth scene: Located inside the enzyme, visualizing the mechanism of the reaction
        :return:
        """
        # Get the objects
        background = Background('color', [0.35, 0.16, 0.2])
        citrate = self.probj.citrate
        camera = Camera('location', [0, 0, -30], 'look_at', [0, 0, 0])
        lighting = LightSource([0, 0, -20], 'color', [1, 1, 1])

        # Split respective OH and H atoms from citrate and move away
        if step <= 90:
            offset = self.prfunc.get_distance(step, self.dur[3] / 3, [3, 0, 0])
            oh_group = citrate.divide([5, 15], 'oh_group', offset=offset)  # Split OH
            h_atom = citrate.divide([13], 'h_atom', offset=offset)  # Split H

        # Switch OH and H atoms + rotate OH group
        elif step <= 180:
            oh_group = citrate.divide([5, 15], 'oh_group', offset=[6, 0, 0])
            h_atom = citrate.divide([13], 'h_atom', offset=[6, 0, 0])
            # Distances for moving the OH and H up and down
            moving_up = self.prfunc.get_distance(step, self.dur[3] / 3, [0, 2, -0.55], 3)
            moving_down = self.prfunc.get_distance(step, self.dur[3] / 3, [0, -1.5, 0.39], 3)
            # Move H atom
            h_atom.move_offset(moving_down)
            # Rotate OH group while moving
            oh_group.move_offset(moving_up)
            self.prfunc.rotate_molecule(0.5, oh_group, (self.dur[3] / 3) * 30, step - 90)

        # Move OH and H atoms back towards molecule
        else:
            oh_group = citrate.divide([5, 15], 'oh_group', offset=[6, 2.1, -0.6])
            h_atom = citrate.divide([13], 'h_atom', offset=[6, -1.5, 0.39])
            self.prfunc.rotate_molecule(0.5, oh_group, (self.dur[3] / 3) * 30, 90)  # Rotation OH
            # Distance for moving OH and H inwards
            inwards_oh = self.prfunc.get_distance(step, self.dur[3] / 3, [-9.5, 0, 0], 6)
            inwards_h = self.prfunc.get_distance(step, self.dur[3] / 3, [-4, 0, 0], 6)
            # Move OH and H inwards
            oh_group.move_offset(inwards_oh)
            h_atom.move_offset(inwards_h)

        # List of objects to render
        objects = citrate.povray_molecule + oh_group.povray_molecule + h_atom.povray_molecule + \
                  [background] + [lighting]

        return Scene(camera, objects=objects)

    def s5_fading_out(self, step):
        """
        Fifth scene: Isocitrate is made, light fades out, moving out of the enzyme
        """
        # Dim lights inside the enzyme
        if step <= 60:
            # Get the objects
            isocitrate = self.probj.isocitrate
            background = Background('color', [0.35, 0.16, 0.2])
            camera = Camera('location', [0, 0, -30], 'look_at', [0, 0, 0])
            # Light fading
            intensity = self.prfunc.get_distance(step, self.dur[4] / 3, [-1, -1, -1])
            intensity[:] = [number + 1 for number in intensity]  # Same negative error
            # Light fade out
            lighting = LightSource([0, 0, -20], 'color', intensity)
            # List of objects to render
            objects = [background] + [lighting] + isocitrate.povray_molecule

        # Move out of the enzyme
        else:
            # Get the objects
            enzyme = self.probj.enzyme
            lighting = LightSource([30, 0, -20], 'color', [1, 1, 1])
            # Move the camera backwards, out of the enzyme
            position = self.prfunc.get_distance(step, self.dur[4], [0, 0, -30], 2)
            position[0] = 35
            position[2] -= 5
            camera = Camera('location', position, 'look_at', [30, 0, 0])
            # List of objects to render
            objects = enzyme + [lighting]

        return Scene(camera, objects=objects)

    def s6_final(self, step):
        """
        Sixth and final scene: Move isocitrate out of the enzyme,
        rotation of isocitrate for visualization
        """
        # Get the objects
        isocitrate = self.probj.isocitrate
        lighting = LightSource([30, 0, -20], 'color', [1, 1, 1])
        enzyme = self.probj.enzyme

        # Move isocitrate out of the enzyme, camera focuses on isocitrate
        if step <= 60:
            position = self.prfunc.get_distance(step, self.dur[5] / 3, [20, 0, 0])
            position[0] += 31  # Set start position of isocitrate at [31, 0, 0]
            isocitrate.move_offset(position)
            camera = Camera('location', [35, 0.0, -25], 'look_at', position)

        # Rotation isocitrate for visualization
        else:
            isocitrate.move_offset([51, 0, 0])
            camera = Camera('location', [35, 0.0, -25], 'look_at', [51, 0, 0])
            self.prfunc.rotate_molecule(2, isocitrate, ((self.dur[5] / 3) * 2) * 30, step - 60)

        # List of objects to render
        objects = isocitrate.povray_molecule + enzyme + [lighting]

        return Scene(camera, objects=objects)


def main(step):
    """
    Main function
    """
    tf_end = [120, 240, 420, 690, 870, 1050]
    # Scenes   1    2    3    4    5     6

    # Initialize functions
    probj = PovRayObjects()
    prfunc = PovRayFunctions(tf_end)
    # Get the time frames
    tf_start, tf_dur = prfunc.get_timesframes()
    tf_dur[:] = [number / 30 for number in tf_dur]
    # Initialize the scenes
    prscenes = PovRayScenes(probj, prfunc, tf_start, tf_dur, tf_end)

    # Create the scenes according to step
    if step <= tf_end[0]:
        scene = prscenes.s1_citrate_rotation(step)
    elif step <= tf_end[1]:
        scene = prscenes.s2_moving(step - tf_end[0])
    elif step <= tf_end[2]:
        scene = prscenes.s3_fading_in(step - tf_end[1])
    elif step <= tf_end[3]:
        scene = prscenes.s4_switching(step - tf_end[2])
    elif step <= tf_end[4]:
        scene = prscenes.s5_fading_out(step - tf_end[3])
    else:
        scene = prscenes.s6_final(step - tf_end[4])
    return scene


if __name__ == "__main__":
    # for i in range(1000, 1050):
    #     pypovray.render_scene_to_png(main, i)

    pypovray.render_scene_to_png(main, i)
