/***************************************************************************************************
* UvcH264.h - Definitions of the UVC H.264 Payload specification Version 1.0
*
*             Copyright (c) 2011 USB Implementers Forum, Inc.
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
* THE SOFTWARE.
****************************************************************************************************/

#ifndef _UVC_H264_H_
#define _UVC_H264_H_
#ifndef WIN32
  typedef unsigned int DWORD;
  typedef unsigned short WORD;
  typedef unsigned char BYTE;
#endif
/* Header File for the little-endian platform */

/* Global Defines */

/* bmHints defines */

#define BMHINTS_RESOLUTION        (0x0001)
#define BMHINTS_PROFILE           (0x0002)
#define BMHINTS_RATECONTROL       (0x0004)
#define BMHINTS_USAGE             (0x0008)
#define BMHINTS_SLICEMODE         (0x0010)
#define BMHINTS_SLICEUNITS        (0x0020)
#define BMHINTS_MVCVIEW           (0x0040)
#define BMHINTS_TEMPORAL          (0x0080)
#define BMHINTS_SNR               (0x0100)
#define BMHINTS_SPATIAL           (0x0200)
#define BMHINTS_SPATIAL_RATIO     (0x0400)
#define BMHINTS_FRAME_INTERVAL    (0x0800)
#define BMHINTS_LEAKY_BKT_SIZE    (0x1000)
#define BMHINTS_BITRATE           (0x2000)
#define BMHINTS_ENTROPY           (0x4000)
#define BMHINTS_IFRAMEPERIOD      (0x8000)

/* wSliceMode defines */

#define SLICEMODE_BITSPERSLICE    (0x0001)
#define SLICEMODE_MBSPERSLICE     (0x0002)
#define SLICEMODE_SLICEPERFRAME   (0x0003)

/***********************************************************************************************************************
* bUsageType defines
* The bUsageType used in Probe/Commit structure. The UCCONFIG parameters are based on "UCConfig Modes v1.1".
* bUsageType  UCConfig   Description
*   4           0        Non-scalable single layer AVC bitstream with simulcast(number of simulcast streams>=1)
*   5           1        SVC temporal scalability with hierarchical P with simulcast(number of simulcast streams>=1)
*   6           2q       SVC temporal scalability + Quality/SNR scalability with simulcast(number of simulcast streams>=1)
*   7           2s       SVC temporal scalability + spatial scalability with simulcast(number of simulcast streams>=1)
*   8           3        Full SVC scalability (temporal scalability + SNR scalability + spatial scalability)
*                        with simulcast(number of simulcast streams>=1)
************************************************************************************************************************/

#define USAGETYPE_REALTIME        (0x01)
#define USAGETYPE_BROADCAST       (0x02)
#define USAGETYPE_STORAGE         (0x03)
#define USAGETYPE_UCCONFIG_0      (0x04)
#define USAGETYPE_UCCONFIG_1      (0x05)
#define USAGETYPE_UCCONFIG_2Q     (0x06)
#define USAGETYPE_UCCONFIG_2S     (0x07)
#define USAGETYPE_UCCONFIG_3      (0x08)

/* bRateControlMode defines */

#define RATECONTROL_CBR           (0x01)
#define RATECONTROL_VBR           (0x02)
#define RATECONTROL_CONST_QP      (0x03)
#define RATECONTROL_FIXED_FRM_FLG (0x10)

/* bStreamFormat defines */

#define STREAMFORMAT_ANNEXB       (0x00)
#define STREAMFORMAT_NAL          (0x01)

/* bEntropyCABAC defines */

#define ENTROPY_CAVLC             (0x00)
#define ENTROPY_CABAC             (0x01)

/* bTimingstamp defines */

#define TIMESTAMP_SEI_DISABLE     (0x00)
#define TIMESTAMP_SEI_ENABLE      (0x01)

/* bPreviewFlipped defines */

#define PREFLIPPED_DISABLE        (0x00)
#define PREFLIPPED_HORIZONTAL     (0x01)


/* wLayerID Macro */

/*                              wLayerID
  |------------+------------+------------+----------------+------------|
  |  Reserved  |  StreamID  | QualityID  |  DependencyID  | TemporalID |
  |  (3 bits)  |  (3 bits)  | (3 bits)   |  (4 bits)      | (3 bits)   |
  |------------+------------+------------+----------------+------------|
  |15        13|12        10|9          7|6              3|2          0|
  |------------+------------+------------+----------------+------------|
*/

#define xLayerID(stream_id, quality_id, dependency_id, temporal_id) ((((stream_id)&7)<<10)|(((quality_id)&7)<<7)|(((dependency_id)&15)<<3)|((temporal_id)&7))

/* id extraction from wLayerID */

#define xStream_id(layer_id)      (((layer_id)>>10)&7)
#define xQuality_id(layer_id)     (((layer_id)>>7)&7)
#define xDependency_id(layer_id)  (((layer_id)>>3)&15)
#define xTemporal_id(layer_id)    ((layer_id)&7)



#define UVC_SET_CUR                                     0x01
#define UVC_GET_CUR                                     0x81
#define UVC_GET_MIN                                     0x82
#define UVC_GET_MAX                                     0x83
#define UVC_GET_RES                                     0x84
#define UVC_GET_LEN                                     0x85
#define UVC_GET_INFO                                    0x86
#define UVC_GET_DEF                                     0x87



/*
 usage:
    CONFIG_PROBE/GET_whatever
    patch it
    CONFIG_PROBE/SET_CUR
    CONFIG_PROBE/GET_CUR
    check it
    CONFIG_COMMIT/SET_CUR
 */
/* UVC H.264 control selectors */

typedef enum _uvcx_control_selector_t
{
	UVCX_VIDEO_CONFIG_PROBE			= 0x01,
	UVCX_VIDEO_CONFIG_COMMIT		= 0x02,
	UVCX_RATE_CONTROL_MODE			= 0x03,
	UVCX_TEMPORAL_SCALE_MODE		= 0x04,
	UVCX_SPATIAL_SCALE_MODE			= 0x05,
	UVCX_SNR_SCALE_MODE				= 0x06,
	UVCX_LTR_BUFFER_SIZE_CONTROL	= 0x07,
	UVCX_LTR_PICTURE_CONTROL		= 0x08,
	UVCX_PICTURE_TYPE_CONTROL		= 0x09,
	UVCX_VERSION					= 0x0A,
	UVCX_ENCODER_RESET				= 0x0B,
	UVCX_FRAMERATE_CONFIG			= 0x0C,
	UVCX_VIDEO_ADVANCE_CONFIG		= 0x0D,
	UVCX_BITRATE_LAYERS				= 0x0E,
	UVCX_QP_STEPS_LAYERS			= 0x0F,
} uvcx_control_selector_t;


typedef struct _uvcx_video_config_probe_commit_t
{
	DWORD	dwFrameInterval;
	DWORD	dwBitRate;
	WORD	bmHints;
	WORD	wConfigurationIndex;
	WORD	wWidth;
	WORD	wHeight;
	WORD	wSliceUnits;
	WORD	wSliceMode;
	WORD	wProfile;
	WORD	wIFramePeriod;
	WORD	wEstimatedVideoDelay;
	WORD	wEstimatedMaxConfigDelay;
	BYTE	bUsageType;
	BYTE	bRateControlMode;
	BYTE	bTemporalScaleMode;
	BYTE	bSpatialScaleMode;
	BYTE	bSNRScaleMode;
	BYTE	bStreamMuxOption;
	BYTE	bStreamFormat;
	BYTE	bEntropyCABAC;
	BYTE	bTimestamp;
	BYTE	bNumOfReorderFrames;
	BYTE	bPreviewFlipped;
	BYTE	bView;
	BYTE	bReserved1;
	BYTE	bReserved2;
	BYTE	bStreamID;
	BYTE	bSpatialLayerRatio;
	WORD	wLeakyBucketSize;
} uvcx_video_config_probe_commit_t;


typedef struct _uvcx_rate_control_mode_t
{
	WORD	wLayerID;
	BYTE	bRateControlMode;
} uvcx_rate_control_mode_t;


typedef struct _uvcx_temporal_scale_mode_t
{
	WORD	wLayerID;
	BYTE	bTemporalScaleMode;
} uvcx_temporal_scale_mode_t;


typedef struct _uvcx_spatial_scale_mode_t
{
	WORD	wLayerID;
	BYTE	bSpatialScaleMode;
} uvcx_spatial_scale_mode_t;


typedef struct _uvcx_snr_scale_mode_t
{
	WORD	wLayerID;
	BYTE	bSNRScaleMode;
	BYTE	bMGSSublayerMode;
} uvcx_snr_scale_mode_t;


typedef struct _uvcx_ltr_buffer_size_control_t
{
	WORD	wLayerID;
	BYTE	bLTRBufferSize;
	BYTE	bLTREncoderControl;
} uvcx_ltr_buffer_size_control_t;

typedef struct _uvcx_ltr_picture_control
{
	WORD	wLayerID;
	BYTE	bPutAtPositionInLTRBuffer;
	BYTE	bEncodeUsingLTR;
} uvcx_ltr_picture_control;


typedef struct _uvcx_picture_type_control_t
{
	WORD	wLayerID;
	WORD	wPicType;
} uvcx_picture_type_control_t;


typedef struct _uvcx_version_t
{
	WORD	wVersion;
} uvcx_version_t;


typedef struct _uvcx_encoder_reset
{
	WORD	wLayerID;
} uvcx_encoder_reset;


typedef struct _uvcx_framerate_config_t
{
	WORD	wLayerID;
	DWORD	dwFrameInterval;
} uvcx_framerate_config_t;


typedef struct _uvcx_video_advance_config_t
{
	WORD	wLayerID;
	DWORD	dwMb_max;
	BYTE	blevel_idc;
	BYTE	bReserved;
} uvcx_video_advance_config_t;


typedef struct _uvcx_bitrate_layers_t
{
	WORD	wLayerID;
	DWORD	dwPeakBitrate;
	DWORD	dwAverageBitrate;
} uvcx_bitrate_layers_t;


typedef struct _uvcx_qp_steps_layers_t
{
	WORD	wLayerID;
	BYTE	bFrameType;
	BYTE	bMinQp;
	BYTE	bMaxQp;
} uvcx_qp_steps_layers_t;


#ifdef _WIN32
// GUID of the UVC H.264 extension unit: {A29E7641-DE04-47E3-8B2B-F4341AFF003B}
DEFINE_GUID(GUID_UVCX_H264_XU, 0xA29E7641, 0xDE04, 0x47E3, 0x8B, 0x2B, 0xF4, 0x34, 0x1A, 0xFF, 0x00, 0x3B);
#endif

#endif  /*_UVC_H264_H_*/
