#encoding=utf-8
#!/usr/bin/env python3
def get_opus_data(self, convert_rate=None, convert_width=None):
    """
    Returns a byte string representing the contents of a FLAC file containing the audio represented by the ``AudioData`` instance.

    Note that 32-bit FLAC is not supported. If the audio data is 32-bit and ``convert_width`` is not specified, then the resulting FLAC will be a 24-bit FLAC.

    If ``convert_rate`` is specified and the audio sample rate is not ``convert_rate`` Hz, the resulting audio is resampled to match.

    If ``convert_width`` is specified and the audio samples are not ``convert_width`` bytes each, the resulting audio is converted to match.

    Writing these bytes directly to a file results in a valid `FLAC file <https://en.wikipedia.org/wiki/FLAC>`__.
    """
    path = '/Users/riemann/Documents/riemann/audios/lee1.wav'
    process = subprocess.Popen([  # TODO:opus的格式是不是也可以这样搞？
        flac_converter,
        "--stdout", "--totally-silent",
        # put the resulting FLAC file in stdout, and make sure it's not mixed with any program output
        "--best",  # highest level of compression available
        "-",  # the input FLAC file contents will be given in stdin
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=startup_info)
    flac_data, stderr = process.communicate(wav_data)
    return flac_data

 def recognize_baidu(self, audio_data, key=None, language="zh-CN", show_all=True):
        """
        百度语音识别API，
        :param audio_data:
        :param key:
        :param language:语种选择，中文=zh、粤语=ct、英文=en，不区分大小写，默认中文
        :param show_all:
        :return:
        """
        #TODO:listen时，百度识别的问题："黑色的天窗"识别不准、长语音不准、静音或音量不大会出现recognition error、说话不能随意只能清楚的发音；解决健壮性的问题
        assert isinstance(audio_data, AudioData), "Data must be audio data"

        import urllib2
        import pycurl

        print '此次识别开始...'
        begin_time = time.time()

        def get_token():
            apiKey = "0XyzNfIwZeSqDN8oZWR54Qon"
            secretKey = "92971d401d3df1bd2869afebc04df63b"

            auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials" + \
                       "&client_id=" + apiKey + "&client_secret=" + secretKey

            res = urllib2.urlopen(auth_url)
            json_data = res.read()
            return json.loads(json_data)['access_token']

        global baidu_text
        def dump_res(buf):
            global baidu_text
            a = eval(buf)
            if a['err_msg'] == 'success.':
                # print a['result'][0]#终于搞定了，在这里可以输出，返回的语句
                baidu_text = a['result'][0]
            else:
                baidu_text = a['err_msg'] if not show_all else a

        wav_data = audio_data.get_wav_data(
            convert_rate=16000,  # audio samples must be at least 8 kHz
            convert_width=2  # audio samples should be 16-bit
        )
        audio_len = len(wav_data)
        cuid = "38:c9:86:13:93:1f"  # my Mac MAC
        token = get_token()
        srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token
        http_header = [
            'Content-Type: audio/wav;rate=16000',
            'Content-Length: %d' % audio_len      ]

        c = pycurl.Curl()
        c.setopt(pycurl.URL, str(srv_url))  # curl doesn't support unicode
        #c.setopt(c.RETURNTRANSFER, 1)
        c.setopt(c.HTTPHEADER, http_header)  # must be list, not dict
        c.setopt(c.POST, 1)
        c.setopt(c.CONNECTTIMEOUT, 300)
        c.setopt(c.TIMEOUT, 30)
        c.setopt(c.WRITEFUNCTION, dump_res)
        c.setopt(c.POSTFIELDS, wav_data)
        c.setopt(c.POSTFIELDSIZE, audio_len)
        # c.setopt(c.VERBOSE, True)
        try:
            c.perform()  # pycurl.perform() has no return val
        except Exception,e:
            raise Exception(":"+e.message)#not very good
        finally:
            c.close()

        end_time = time.time()
        recognition_time = end_time-begin_time

        print baidu_text,'时间：{:.2f}s\n'.format(recognition_time)
        # return baidu_text