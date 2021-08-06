#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('/studio/tools/py/studio')
sys.path.append('/studio/tools/py/')
sys.path.append('/studio/tools/code/release')
import os
import subprocess
import re
import signal
import fnmatch
import xmlrpclib
import shlex
import shutil
import time
import datetime
import json
import PIL.Image
from threading import Thread

import html2text
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from st_utils import coloured_logs as clogs
import thumbnail as thumbnail
import view_in_cut
from thumbnail_multi import Thumbnailer
import commandor_tools

PADDING = int(os.environ['ALG_VER_PADDING']) if 'ALG_VER_PADDING' in os.environ else 4

####

id_string = datetime.datetime.now().strftime("%H-%M-%S")
ffstats = os.path.expanduser(("~/ffstats" + id_string))


def print_inside(me):
    print("*"*80)
    print(me)
    print("^"*80)


class MyThread(Thread):
    def __init__(self, command):
        Thread.__init__(self)
        self.command = command

    def run(self):
        os.system(self.command)
        print_inside("DONE WITH %s" % self.command)


server = '/studio/proj/'
proj_conv = '.proj_conventions'
dailies_dir = "dailies"


class DailiesCreator():
    '''
    return daily from jpgs counting from 1
    '''

    def __init__(self, path, notes, proj, kmb , usr_name ):
        self.seq_path = path
        self.notes = notes
        self.tech = False
        self.letterboxing = True
        self._proj = proj
        self._kmb = kmb
        self._artist_name = usr_name
        self.daily_name = "__".join(list(reversed(self._kmb.split("__"))))
        self.cerebro_url = self._kmb.replace("__", "/")
        self._version = self.get_the_version()
        self.daily_path = ""
        self.proj_conv = {}

    def get_file_list_len(self):
        p = self.seq_path.rsplit("%")[-1]
        ff = int(p.rsplit(" ")[1])
        lf = int(p.rsplit(" ")[2])
        return lf - ff + 1

    def get_proj_conventions(self):
        '''
        return keys as dict
        '''
        proj = self._proj
        history_fnm = os.path.join(server, proj, "project.json")
        # keys
        keys = dict(zip((
            'resolution',
            'fontsize',
            'slate',
            'cache',
            'cacheIntensity',
            'fps'),
            ('1280x720',
             '16',
             '1',
             'Low',
             '25',
             )))
        if not self.proj_conv:
            if os.path.exists(history_fnm):
                with open(history_fnm, 'rb') as fp:
                    self.proj_conv = json.load(fp)
        return self.proj_conv

    def get_thumbs(self):
        mt = self.get_file_mimetype()
        if mt.split('/')[0] == 'video':
            self.make_thumnails_from_video()
        elif mt.split('/')[0] == 'image':
            self.make_thumnails_from_image()
        return self.return_thumbs_list()

    def nk_from_sequence(self, filepath):
        """
        Args:
            filepath (str) - first frame in sequence
        """
        ext = os.path.splitext(filepath)[-1]
        if os.path.isfile(filepath) and ext.lower() in ['.jpg','.jpeg']:
            img = PIL.Image.open(filepath)
            exif = img._getexif()
            if exif and 270 in exif: # 270 is for exif/0/ImageDescription
                return str(exif[270])
        return ""

    def locate(self, pattern, root=os.curdir, choice=2, obj_type="files"):
        '''
        Yields generator, which helps to locate files by glob pattern
        Args:
            pattern (str): file pattern
            root (str): where to search
            choice (int): defines what to yield
            obj_type (str): 
        Yields:
            item (generator)
        '''
        # print(os.path.abspath(root))
        for path, dirs, files in os.walk(os.path.abspath(root)):
            if obj_type == "dirs":
                iterables = dirs
            else:
                iterables = files
            for item in [n for n in iterables if fnmatch.fnmatch(n.upper(), pattern.upper())]:
                if choice == 1:
                    yield os.path.join(path, item)
                if choice == 2:
                    yield path
                if choice == 3:
                    yield path, item
                else:
                    yield item

    def get_the_version(self):
        mov_files = []
        proj = self._proj
        vfxname =self._kmb
        dailies_path = os.path.join(server, proj, dailies_dir)
        #wildcard = "*" + vfxname + "*"
        wildcards = ["{}_V{}.mov".format(vfxname, "[0-9]" * (PADDING - 2)),\
                   "{}_V{}_tech.mov".format(vfxname, "[0-9]" * (PADDING - 2)),\
                   "{}_V{}.mov".format(vfxname, "[0-9]" * PADDING),\
                   "{}_V{}_tech.mov".format(vfxname, "[0-9]" * PADDING),\
                   "{}_V{}.out_srgb.mov".format(vfxname, "[0-9]" * PADDING),\
                   "{}_V{}_tech.out_srgb.mov".format(vfxname, "[0-9]" * PADDING)]
        # Locating last daily version
        for wildcard in wildcards:
            print("Searching for last daily %s %s %s" % (proj, wildcard, dailies_path))
            for mov_file in self.locate(wildcard, dailies_path, 3):
                if mov_file[-1].endswith('.mov') and not mov_file[-1].startswith('.'):
                    mov_files.append(os.path.join(mov_file[0], mov_file[1]))
                    print(os.path.join(mov_file[0], mov_file[1]))
        mov_versions = sorted(
            set([int(os.path.splitext(os.path.basename(i))[0]\
                .replace("_tech", "")\
                .replace(".mov", "")\
                .replace(".out_srgb", "")\
                .rsplit("_V", 1)[-1]) for i in mov_files])) #TODO: replace by regexp
        if mov_versions == []:
            last_daily_ver = 0
        else:
            last_daily_ver = mov_versions[-1]
        print("\nLatest daily has version V{}".format(last_daily_ver))

        # Now defining new daily ver
        if int(last_daily_ver) == 0:
            createVersion = "1".zfill(PADDING)
        else:
            createVersion = str(last_daily_ver + 1).zfill(PADDING)
        return createVersion

    def return_file_list_from_seq(self, sequence_w_range):
        """
        Generates file list with full paths
        
        Args:
            sequence_w_range: str formatted to reflect sequence start and end
                frames. For example: `/path/to/seq.%06d.exr@1001@1100`
                Only full absolute paths accepted!

        Returns:
            frames_list: List[str] of full paths to each frame in sequence
        """
        print(sequence_w_range)
        first = sequence_w_range.split('@')[1]
        last = sequence_w_range.split('@')[2]
        seq = sequence_w_range.split('@')[0]
        padding_int = seq.rsplit('%', 1)[-1][:2]
        padding = '%' + padding_int + 'd'
        renderpath = seq.split(padding)[0]
        trailing = seq.split(padding)[-1]
        frames_list = []
        for i in xrange(int(first), int(last) + 1):
            f = renderpath + str(i).zfill(int(padding_int)) + trailing
            frames_list.append(f)
        return sorted(frames_list, key=self.keynat)

    def keynat(self, l):
        return [[
                pp[0] if p[0] else int(pp[1])
                for pp in re.findall(r'(\\D+)|(\\d+)', p)
                ]
            for p in l.strip().split('/')
        ]



    def get_img_width_and_height(self, fileloc) :
        command = ['ffprobe', '-v', 'quiet', '-show_entries',
            'stream=width,height', '-of', 'default=noprint_wrappers=1:nokey=1',
            fileloc, '-sexagesimal']
        clogs.say(" ".join(command), 5)
        ffmpeg = subprocess.Popen(command, stderr=subprocess.PIPE, 
            stdout = subprocess.PIPE)
        out, err = ffmpeg.communicate()
        if(err) : print(err)
        if out != '':
            out = out.split('\n')
            print(out)
            return {'width': int(out[0]),
                    'height' : int(out[1])}
        else:
            return {'width': 0,
                    'height': 0}

    def cache_intensity_to_color(self, intensity="Medium"):
        if intensity == "High":
            cacheClr = "xc:#000000CC"
        if intensity == "Medium":
            cacheClr = "xc:'rgba(0,0,0, 0.4)'"
        if intensity == "Low":
            cacheClr = "xc:'rgba(0,0,0, 0.05)'"
        return cacheClr

    def create_daily(self):
        date = str(time.localtime()[0]) + "." + str(time.localtime()\
            [1]).zfill(2) + "." + str(time.localtime()[2]).zfill(2)
        project = self._proj
        kmb = self._kmb
        version = "_V" + self._version
        extension_mov = ".mov"
        notes = self.notes.rsplit('$status:', 1)[0]
        status = self.notes.rsplit('$status:', 1)[-1]
        fontToUse = '/studio/tools/nuke/nuke_tools/fonts/DroidSans.ttf'

        fileRead = self.seq_path
        sequence_l = fileRead
        sequence = fileRead.rsplit(' ', 2)[0]
        first_frame = fileRead.rsplit(' ', 2)[1]
        count_frame_start = first_frame
        last_frame = fileRead.rsplit(' ', 2)[2]
        padding = int(sequence.split("%")[-1][1:2])
        nk_source = self.nk_from_sequence(sequence % int(first_frame))
        # mime type todo
        
        one_of_the_files = sequence.split("%")[0] + first_frame.zfill(padding)\
            + sequence.split("%")[-1][3:]
        tt = self.get_img_width_and_height(one_of_the_files)
        sWidth = int(tt['width'])  # source width
        sHeight = int(tt['height'])  # source height
        scale = self.get_proj_conventions()['dailies']['resolution']
        
        if scale and not scale == 'As input':
            width = int(scale.split("x")[0])
            height = int(scale.split("x")[1])
        else:
            width = sWidth
            height = sHeight

        if not sequence.endswith('.jpg') or not first_frame == '1' or (width != sWidth or height != sHeight):
            # need to convert
            seq = '@'.join(self.seq_path.rsplit(' ', 2))
            files = self.return_file_list_from_seq(seq)
            temp_dir = '/tmp/' + id_string
            os.mkdir(temp_dir)
            padding = 6
            # EXR
            if one_of_the_files.lower().endswith('.exr'):
                aces = str(self.get_proj_conventions()['pipeline']['aces'])
                colorspace = self.get_proj_conventions()['colorspace'].replace(' ', '!@!')
                command = '/studio/tools/nuke/nukex -t /studio/tools/py/studio/daily_nuke.py %s %s %s %s %s %s' % (self.seq_path, scale.replace(' ', ''), padding, temp_dir, aces, colorspace)
                os.system(command)
                if width == sWidth:
                    try:
                        f = open('/tmp/' + id_string +  '_size.txt', 'r')
                    except:
                        print('Failed to read to file size')
                    size = f.read()
                    width = int(size.split('\n')[0])
                    height = int(size.split('\n')[1])
                    f.close()
            else:
                # JPG
                index = 1
                resize_params = ""
                if (width != sWidth or height != sHeight):
                    resize_params = "-resize %sx" % width
                for i in files:
                    current_frame = str(index).zfill(padding)
                    current_name = os.path.join(temp_dir, current_frame+'.jpg')
                    if i.lower().endswith('.dpx'):
                        command = 'convert %s %s -set colorspace log -colorspace sRGB %s' % (resize_params, i, current_name)
                    #elif i.lower().endswith('.exr'):
                    #    command = 'convert %s -gamma 2.2 %s -colorspace sRGB %s' % (resize_params, i, current_name)
                    else:
                        command = 'convert %s %s -colorspace sRGB -colorspace sRGB -strip %s' % (resize_params, i, current_name)
                    index += 1
                    clogs.say(command, 5)
                    os.system(command)
            first_frame = str(1)
            last_frame = len(files)
            sequence = os.path.join(temp_dir, '%0'+str(padding)+'d.jpg')
            sequence_l = '%s %s %s' % (sequence, first_frame, last_frame)

        slateFrame = str(0)
        slatePath = sequence.split(
            "%")[0] + slateFrame.zfill(padding) + sequence.split("%")[-1][3:]

        ########### find the image size #################
        #ratio = float(size.split('x')[0]) / float(size.split('x')[1])
        one_of_the_files = sequence.split("%")[0] + first_frame.zfill(padding) + sequence.split("%")[-1][3:]
        tt = self.get_img_width_and_height(one_of_the_files)
        sWidth = int(tt['width'])  # source width
        sHeight = int(tt['height'])  # source height

        # get project settings
        slate = self.get_proj_conventions()['dailies']['slate']
        cache = float(self.get_proj_conventions()['dailies']['cache'])
        fontsize = int(self.get_proj_conventions()['dailies']['fontsize'])
        fps = self.get_proj_conventions()['fps']
        cache_intensity = self.get_proj_conventions()[
            'dailies']['cacheIntensity']
        cacheClr = self.cache_intensity_to_color(cache_intensity)

        coefficient = width / 600.0
        height_coefficient = sHeight / 1000.0
        fontsize *= coefficient

        cacheHeight = '0'
        if self.letterboxing == False:
            print("LETTERBOXING DISABLED")
            cacheHeight = "0"
        elif width / cache < height:
            cacheHeight = str(int((height - width / cache) / 2))

        date = datetime.date.today().strftime("%Y.%m.%d")
        length = str(int(last_frame) - int(first_frame) + 1)
        sAspect = sWidth / float(sHeight)
        aspect = width / float(height)
        padY = int(sWidth / aspect)
        padPanY = (padY-sHeight) / 2
        cropHeight = int(sWidth / aspect)
        artist = self._artist_name

        slateJpg = '/tmp/slate_%s.jpg' % id_string
        frame_png = '/tmp/frame_%s.jpg' % id_string
        canvasPng = '/tmp/canvas_%s.png' % id_string
        result = '/tmp/result_%s.png' % id_string
        slateJPG_MOV = '/tmp/slate_movie_%s.mov' % id_string
        body_MOV = '/tmp/body_movie_%s.mov' % id_string

        dailies_path = os.path.join(server, project, dailies_dir, date)

        if self.tech == True:
            daily_name = self.daily_name + version + "_tech" + extension_mov
        else:
            daily_name = self.daily_name + version + extension_mov
        daily_path = os.path.join(dailies_path, daily_name)

        self.daily_path = daily_path   # return daily path before rendering it
        if not os.path.exists(dailies_path):
            os.mkdir(dailies_path)
        os.system("touch %s" % daily_path)

        # CANVAS
        if project != "FAU":
            canvas_templ = "/studio/tools/py/studio/canvas_template.sh"
        else:
            canvas_templ = "/studio/tools/py/studio/canvas_template_FAU.sh"
            if self.letterboxing == True:
                cacheHeight = str(int((width - height * 1.43) / 2))
            else:
                cacheHeight = '0'
            cacheClr = "xc:'rgba(0,0,0, 0.7)'"
        with open(canvas_templ) as f:
            data = f.read()

        version_str = "%s   %s" % (version, date)
        data = data.replace("$width$", str(width)).replace(
            "$height$", str(height)).replace("$cacheHeight$", str(cacheHeight))
        data = data.replace("$canvasPng$", canvasPng)
        data = data.replace("$cacheClr$", cacheClr)
        # data = data.replace("$VERSION$", version_str )
        data = data.replace("$PROJECT$", project)
        data = data.replace("$ARTIST$", artist)
        data = data.replace("$KMB$", kmb.replace("__", "|"))
        data = data.replace("$FONT$", str(fontsize / 2))
        data = data.replace("$VERSION$", version_str[1:])  # strip first sign

        # END CANVAS

        # FFMPEG COMMAND
        ff_command = ""
        if sAspect < aspect: 
            print("DEBUG: "+str(sWidth)+':'+str(cropHeight)+',scale='+str(width)+':'+str(height)+": END DEBUG!")
            ff_command += 'ffmpeg -y -f image2 -framerate ' + fps + ' -i ' + sequence + ' -vf "crop='+str(sWidth)+':'+str(cropHeight)+',scale='+str(width)+':'+str(height)+'" -f image2pipe -vcodec ppm - | ffmpeg -vstats_file ' + ffstats + ' -loglevel quiet -framerate '+fps+' -f image2pipe -vcodec ppm -i -  -vf "movie=' + canvasPng + \
                ' [watermark]; [in]scale=$width:$height [scale]; [scale][watermark] overlay=0:0,  drawtext=text=%{eif\\\\\\\\:n+' + str(count_frame_start) + '\\\\\\\\:d}: expansion=normal: fontfile=' + \
                fontToUse + \
                ': x=w-tw-5: y=h-lh-5: fontcolor=white: fontsize=$FONT: shadowx=1: shadowy=1 [out]" -f mov -vcodec mjpeg -qscale 1 -y -threads 0 ' + body_MOV + '\n'
        else:
            if project != "FAU":
                ff_command += 'ffmpeg -y -f image2 -framerate ' + fps \
                    + ' -i ' + sequence \
                    + ' -vf "pad=' + str(width) + ':' + str(height) + ':0:' + str(padPanY) \
                    + ',scale=' + str(width) + ':' + str(height) \
                    + '" -f image2pipe -vcodec ppm - | ffmpeg -vstats_file ' + ffstats \
                    + ' -loglevel quiet -framerate ' + fps \
                    + ' -f image2pipe -vcodec ppm -i -  -vf "movie=' + canvasPng \
                    + ' [watermark]; [in]scale=$width:$height [scale]; [scale][watermark] overlay=0:0,  drawtext=text=%{eif\\\\\\\\:n+' + str(count_frame_start) + '\\\\\\\\:d}: expansion=normal: fontfile=' + fontToUse \
                    + ': x=w-tw-5: y=h-lh-5: fontcolor=white: fontsize=$FONT: shadowx=1: shadowy=1 [out]" -f mov -vcodec mjpeg -q:v 2  -y -threads 0 ' + body_MOV + '\n'
            else:
                ff_command += 'ffmpeg -y -f image2 -framerate ' + fps \
                    + ' -i ' + sequence \
                    + ' -vf "pad=' + str(width) + ':' + str(height) + ':0:' + str(padPanY) \
                    + ',scale=' + str(width) + ':' + str(height) \
                    + '" -f image2pipe -vcodec ppm - | ffmpeg -vstats_file ' + ffstats \
                    + ' -loglevel quiet -framerate ' + fps \
                    + ' -f image2pipe -vcodec ppm -i -  -vf "movie=' + canvasPng \
                    + ' [watermark]; [in]scale=$width:$height [scale]; [scale][watermark] overlay=0:0,  drawtext=text=%{eif\\\\\\\\:n+' + str(count_frame_start) + '\\\\\\\\:d}: expansion=normal: fontfile=' + fontToUse \
                    + ': x=w-tw-5-${cache}: y=h-lh-5: fontcolor=white: fontsize=$FONT: shadowx=1: shadowy=1 [out]" -f mov -vcodec mjpeg -q:v 2  -y -threads 0 ' + body_MOV + '\n'
            
        data += ff_command
        render_body_bash = "/tmp/render_body_%s.sh" % id_string
        with open(render_body_bash, 'w') as f:
            f.write(data)
        # END FFMPEG COMMAND
        c = MyThread('bash %s' % render_body_bash)
        c.start()

        # THUMBS
        thmbs = Thumbnailer(sequence_l)
        ext = thmbs.get_thumbs()
        # print("thumbs ready!")
        # print_inside(ext[0])
        # l1 = list(ext[0])
        # l1[-5] = '[1-3]'
        # thumbs="".join(l1)
        thumbs = ext[0].replace("_thumb1", "_thumb[1-3]")

        # SLATE
        render_slate_bash = "/tmp/render_slate_%s.sh" % id_string
        slate_templ = "/studio/tools/py/studio/slate_template.sh"
        with open(slate_templ) as f:
            data = f.read()

        if status == "Final":
            status_color = "green"
        elif status == "SemiFinal":
            status_color = "yellow"
        else:
            status_color = "grey"

        data = data.replace("$width$", str(width)).replace(
            "$height$", str(height))
        data = data.replace("$slateJPG$", slateJpg)
        data = data.replace("$RESULT$", result)
        data = data.replace("$THUMBS$", thumbs)
        data = data.replace("$FRAME_PNG$", frame_png)
        data = data.replace("$VERSION$", version_str[1:])  # strip first sign
        data = data.replace("$PROJECT$",  project)
        data = data.replace("$KMB$",  kmb.replace("__", "\n"))
        data = data.replace("$NKSOURCE$", nk_source)
        data = data.replace("$LENGTH$", length)
        data = data.replace("$FPS$",  fps)
        data = data.replace("$STATUS$",  status)
        data = data.replace("$STATUS_COLOR$",  status_color)
        data = data.replace("$FONT$", str(int(fontsize)))
        data = data.replace("$slateJPG_MOV$",  slateJPG_MOV)
        data = data.replace("$NOTES$", notes)
        with open(render_slate_bash, 'w') as f:
            f.write(data.encode('utf-8'))
        # END SLATE

        # pro = subprocess.Popen(['bash', render_slate_bash  ])
        # pro.wait()
        # daily="/tmp/out.mov"
        pro = subprocess.Popen(['bash', render_slate_bash])
        pro.wait()
        c.join()
        if slate:
            mencoder_command = 'mencoder -nosound -ovc copy -idx -of lavf -o %s %s %s' % (
                daily_path, slateJPG_MOV, body_MOV)
            # mencoder_command = 'ffmpeg -hide_banner -y -i %s -i %s -filter_complex "[0:v:0] [1:v:0] concat=n=2:v=1 [v]" -map "[v]" -vcodec libx264 -crf 24 -pix_fmt yuv420p %s'%(slateJPG_MOV, body_MOV, daily_path)
        else:
            mencoder_command = 'mencoder -nosound -ovc copy -idx -of lavf -o %s %s' % (
                daily_path, body_MOV)

        clogs.say(mencoder_command, 5)
        os.system(mencoder_command)
        
        # Cosmoball stuff
        if self._proj=="Cosmoball":
            if not "_tech_" in daily_path.split("/")[-1]:
                # Copy to "/studio/proj/$PROJ/dailies/to_MRP"
                mrp_daily_dir = os.path.join(server, project, dailies_dir,
                    "to_MRP", date)
                if not os.path.isdir(mrp_daily_dir):
                    try:
                        os.mkdir(mrp_daily_dir, 0777)
                    except OSError:
                        print("Directory %s already exists" % mrp_daily_dir)
                mrp_daily_name = "{}_comp_v{}_out_srgb{}".format(self.daily_name,
                    str(self._version).zfill(4), extension_mov).lower()
                mrp_daily_path = os.path.join(mrp_daily_dir, mrp_daily_name)
                
                # Need to remove slate:
                cmd = "ffmpeg -y -ss %s -i %s -c copy -flags global_header %s"\
                    % (1 / float(fps), daily_path, mrp_daily_path)
                clogs.say(cmd, 5)
                res = os.system(cmd)
                print(res)
                # shutil.copy(daily_path, mrp_daily_path)

        # open the newly created daily
        #os.system('/studio/tools/djv/bin/djv_view.sh {} &'.format(daily_path))  
        return daily_path


in_start=int(1001.0)
in_end=int(1052.0)
in_path=str(" ") + str(in_start)+" " + str(in_end)
in_proj=""
in_notes=""
in_kmb=""
in_user=""



daily_creator = DailiesCreator(in_path, in_notes, in_proj, in_kmb , in_user)
daily_creator.create_daily()


