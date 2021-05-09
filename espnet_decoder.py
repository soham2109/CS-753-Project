import time
import string
import math

import matplotlib.pyplot as plt
import numpy as np
import librosa
import torch
from espnet_model_zoo.downloader import ModelDownloader
from espnet2.bin.asr_inference import Speech2Text


Fs = 16000
"""
the other model option for ASR
("Shinji Watanabe/"
"spgispeech_asr_train_asr_conformer6_n_fft512_hop_length256_"
"raw_en_unnorm_bpe5000_valid.acc.ave")
"""
TAG=("kamo-naoyuki/"
"librispeech_asr_train_asr_conformer6_n_fft512_hop_length256_"
"raw_en_bpe5000_scheduler_confwarmup_steps40000_optim_conflr0.0025_sp_valid.acc.ave"
)



def text_normalizer(text):
	text = text.lower()
	return text.translate(str.maketrans('', '', string.punctuation))


def return_figure(data, sr=Fs):
	fig = plt.figure()
	librosa.display.waveplot(data, sr=sr, alpha=0.5)
	plt.grid(True)
	plt.title("Recorded Waveform")
	return fig


def decode(audio_path, sr=Fs):
	d=ModelDownloader() # Run this for the first time
	speech2text = Speech2Text(**d.download_and_unpack(TAG),
    						  device="cpu",
							  minlenratio=0.0,
							  maxlenratio=0.0,
							  ctc_weight=0.5,
							  beam_size=4,
							  batch_size=0,
							  nbest=1)
	data, _ = librosa.load(audio_path, sr=sr)
	start = time.time()
	complete_text=[]
	# number of data_samples in 10 secs = Fs*10
	# total #10sec_chunks = (total_data_points)/(Fs*10)
	num_chunks = math.floor(len(speech)/(Fs*10))
	for i in range(num_chunks):
		nbests = speech2text(speech[i*Fs*10:(i+1)*Fs*10])
		text, *_ = nbests[0]
		complete_text.append(text_normalizer(text))

	decoding_time = time.time()-start
	decoded_text = " ".join(complete_text)
	return decoded_text, decoding_time, return_figure(data, sr=Fs)


if __name__=="__main__":
	audio_path = "audio.wav"
	decoded_text, decoding_time, _ = decode(audio_path)
	print("The text decoded is:")
	print(decoded_text)
	print("Time taken to decode: {}s".format(decoding_time))
