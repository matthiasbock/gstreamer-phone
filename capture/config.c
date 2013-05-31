/*
 *  V4L2 video capture example
 *
 *  This program can be used and distributed without restrictions.
 *
 *      This program is provided with the V4L2 API
 * see http://linuxtv.org/docs.php for more information
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include <getopt.h>             /* getopt_long() */

#include <fcntl.h>              /* low-level i/o */
#include <unistd.h>
#include <errno.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/mman.h>
#include <sys/ioctl.h>

#include <linux/videodev2.h>
#include <linux/uvcvideo.h>

#include "uvch264.h"

static char *dev_name;
static int fd = -1;
static int bitrate = 0;
static int qp = 0;
static int iframe = 0;
static int rcmode = -1;

static void errno_exit(const char *s)
{
  fprintf(stderr, "%s error %d, %s\n", s, errno, strerror(errno));
  exit(EXIT_FAILURE);
}

static int xioctl(int fh, int request, void *arg)
{
  int r;
  
  do {
    r = ioctl(fh, request, arg);
  } while (-1 == r && EINTR == errno);
  
  return r;
}

static void setBitrate(int bmin, int bmax)
{  
  int res;
  struct uvc_xu_control_query ctrl;
  uvcx_bitrate_layers_t  conf;
  ctrl.unit = 12;
  ctrl.size = 10;
  ctrl.selector = UVCX_BITRATE_LAYERS;
  ctrl.data = &conf;
  ctrl.query = UVC_GET_CUR;
  conf.wLayerID = 0;
  conf.dwPeakBitrate = conf.dwAverageBitrate = 0;
  res = xioctl(fd, UVCIOC_CTRL_QUERY, &ctrl);
  if (res)
    {
      perror("ctrl_query");
      return;
    }
  fprintf(stderr, "Bitrate was %d [%d]\n", conf.dwPeakBitrate * 8, conf.dwAverageBitrate * 8);
  conf.dwPeakBitrate = bmax;
  conf.dwAverageBitrate = bmin;
  ctrl.query = UVC_SET_CUR;
  res = xioctl(fd, UVCIOC_CTRL_QUERY, &ctrl);
  if (res)
    {
      perror("ctrl_query");
      return;
    }
  fprintf(stderr, "Bitrate request %d [%d]\n", conf.dwPeakBitrate * 8, conf.dwAverageBitrate * 8);
  ctrl.query = UVC_GET_CUR;
  res = xioctl(fd, UVCIOC_CTRL_QUERY, &ctrl);
  if (res)
    {
      perror("ctrl_query");
      return;
    }
  fprintf(stderr, "Bitrate now %d [%d]\n", conf.dwPeakBitrate * 8, conf.dwAverageBitrate * 8);
}

static void setRCMode(int mode)
{
  int res;
  struct uvc_xu_control_query ctrl;
  uvcx_rate_control_mode_t conf;
  ctrl.selector = UVCX_RATE_CONTROL_MODE;
  ctrl.size = 3;
  ctrl.unit = 12;
  ctrl.data = &conf;
  ctrl.query = UVC_GET_CUR;
  conf.wLayerID = 0;
  res = xioctl(fd, UVCIOC_CTRL_QUERY, &ctrl);
  if (res) { perror("query"); return;}
  fprintf(stderr, "RC mode was %d\n", (int)conf.bRateControlMode);
  conf.bRateControlMode = mode;
  ctrl.query = UVC_SET_CUR;
  res = xioctl(fd, UVCIOC_CTRL_QUERY, &ctrl);
  if (res) { perror("query"); return;}
  fprintf(stderr, "RC mode request %d\n", (int)conf.bRateControlMode);
  ctrl.query = UVC_GET_CUR;
  res = xioctl(fd, UVCIOC_CTRL_QUERY, &ctrl);
  if (res) { perror("query"); return;}
  fprintf(stderr, "RC mode now %d\n", (int)conf.bRateControlMode);
}


void setNextFrame(int frame)
{
  int res;
  struct uvc_xu_control_query ctrl;
  uvcx_picture_type_control_t conf;
  ctrl.selector = UVCX_PICTURE_TYPE_CONTROL;
  ctrl.size = 4;
  ctrl.unit = 12;
  ctrl.data = &conf;
  conf.wLayerID = 0;
  conf.wPicType = frame;
  ctrl.query = UVC_SET_CUR;
  res = xioctl(fd, UVCIOC_CTRL_QUERY, &ctrl);
  fprintf(stderr, "Request IDR frame now.\n");
}

void setQP(int tgt, int qpmin, int qpmax)
{
  int res;
  struct uvc_xu_control_query ctrl;
  uvcx_qp_steps_layers_t conf;
  ctrl.selector = UVCX_QP_STEPS_LAYERS;
  ctrl.size = 5;
  ctrl.unit = 12;
  ctrl.data = &conf;
  ctrl.query = UVC_GET_CUR;
  conf.wLayerID = 0;
  conf.bFrameType = 7;
  conf.bMinQp = conf.bMaxQp = 0;
  res = xioctl(fd, UVCIOC_CTRL_QUERY, &ctrl);
  if (res) { perror("query"); return;}
  fprintf(stderr, "QP was %d / %d\n", (int)conf.bMinQp, (int)conf.bMaxQp);
  conf.bMinQp = qpmin;
  conf.bMaxQp = qpmax;
  conf.bFrameType = tgt;
  ctrl.query = UVC_SET_CUR;
  res = xioctl(fd, UVCIOC_CTRL_QUERY, &ctrl);
  if (res) { perror("query"); return;}
  fprintf(stderr, "QP request %d / %d\n", (int)conf.bMinQp, (int)conf.bMaxQp);
  ctrl.query = UVC_GET_CUR;
  res = xioctl(fd, UVCIOC_CTRL_QUERY, &ctrl);
  if (res) { perror("query"); return;}
  fprintf(stderr, "QP now %d / %d\n", (int)conf.bMinQp, (int)conf.bMaxQp);
}

static void close_device(void)
{
  if (-1 == close(fd))
    errno_exit("close");
  
  fd = -1;
}

static void open_device(void)
{
  struct stat st;
  
  if (-1 == stat(dev_name, &st)) {
    fprintf(stderr, "Cannot identify '%s': %d, %s\n",
	    dev_name, errno, strerror(errno));
    exit(EXIT_FAILURE);
  }
  
  if (!S_ISCHR(st.st_mode)) {
    fprintf(stderr, "%s is no device\n", dev_name);
    exit(EXIT_FAILURE);
  }
  
  fd = open(dev_name, O_RDWR /* required */ | O_NONBLOCK, 0);
  
  if (-1 == fd) {
    fprintf(stderr, "Cannot open '%s': %d, %s\n",
	    dev_name, errno, strerror(errno));
    exit(EXIT_FAILURE);
  }
}

static void usage(FILE *fp, int argc, char **argv)
{
  fprintf(fp,
	  "Usage: %s [options]\n\n"
	  "Version 1.0\n"
	  "Options:\n"
	  "-d | --device name   Video device name [%s]\n"
	  "-b | --bitrate brate Set bitrate in ko/s (only with RC mode = VBR or CBR)\n"
	  "-q | --qp qp         Set QP (only with RC mode = QP)\n"
	  "-i | --iframe        Send an I-Frame now\n"
	  "-r | --rcmode [mode] Set RC mode [VBR, CBR, QP]\n"
	  "",
	  argv[0], dev_name);
}

static const char short_options[] = "d:b:ihr:q:";

static const struct option
long_options[] = {
  { "device",  required_argument, NULL, 'd' },
  { "bitrate", required_argument, NULL, 'b' },
  { "qp", required_argument, NULL, 'q' },
  { "rcmode", required_argument, NULL, 'r' },
  { "iframe", no_argument, NULL, 'i' },
  { "help", no_argument, NULL, 'h' },
  { 0, 0, 0, 0 }
};

int main(int argc, char **argv)
{
  dev_name = "/dev/video0";
  

  if (argc == 1)
    {
      usage(stdout, argc, argv);
      exit(EXIT_SUCCESS);
    }

  for (;; ) {
    int idx;
    int c;
    
    c = getopt_long(argc, argv,
		    short_options, long_options, &idx);
    
    if (-1 == c)
      break;

    switch (c) {
    case 0: /* getopt_long() flag */
      break;
      
    case 'd':
      dev_name = optarg;
      break;
      
    case 'h':
      usage(stdout, argc, argv);
      exit(EXIT_SUCCESS);
      
    case 'i':
      iframe = 1;
      break;
      
    case 'r':
      if (!strcmp(optarg, "VBR"))
	rcmode = RATECONTROL_VBR;
      
      if (!strcmp(optarg, "CBR"))
	rcmode = RATECONTROL_CBR;
      
      if (!strcmp(optarg, "QP"))
	rcmode = RATECONTROL_CONST_QP;
      
      if (rcmode < 0)
	{
	  fprintf(stderr, "Unknown RC mode.\n");
	  usage(stdout, argc, argv);
	  exit(EXIT_SUCCESS);
	}
      
      break;
      
    case 'b':
      errno = 0;
      bitrate = strtol(optarg, NULL, 0);
      if (errno)
	errno_exit(optarg);
      break;

    case 'q':
      errno = 0;
      qp = strtol(optarg, NULL, 0);
      if (errno)
	errno_exit(optarg);
      break;
      
    default:
      usage(stderr, argc, argv);
      exit(EXIT_FAILURE);
    }
  }
  
  open_device();
  
  if (bitrate > 0)
    setBitrate(bitrate / 8, bitrate / 8);
  
  if (iframe)
    setNextFrame(0x01);
  
  if (rcmode >= 0)
    setRCMode(rcmode);

  if (qp > 0)
    setQP(0, qp, qp);

  close_device();
  return 0;
}
