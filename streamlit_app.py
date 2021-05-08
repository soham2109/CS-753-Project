import streamlit as st
#PAGE_CONFIG = {"page_title":"StColab.io","page_icon":":smiley:","layout":"centered"}
#st.beta_set_page_config(**PAGE_CONFIG)
import pyaudio
import wave
import os
import base64

DURATION=10 # record for 10 seconds
MAX_INPUT_CHANNELS=1 # mono audio recording
DEFAULT_SAMPLE_RATE=44100 # 44.1KHz sampling rate default for mic
CHUNKSIZE=8192
WAVE_OUTPUT_FILE="audio.wav"
TEMP_OUTPUT_FILE="audio_16k.wav"
INPUT_DEVICE=0

class record_audio:

	def __init__(self):
		self.stop_audio = 0
		self.recorder = pyaudio.PyAudio()

	def save_recording(self,frames):
		if not frames:
			raise ValueError("No frames recorded.")
		wavfile = wave.open(WAVE_OUTPUT_FILE,"wb")
		wavfile.setnchannels(MAX_INPUT_CHANNELS)
		wavfile.setsampwidth(self.recorder.get_sample_size(pyaudio.paInt16))
		wavfile.setframerate(DEFAULT_SAMPLE_RATE)
		wavfile.writeframes(b''.join(frames))
		wavfile.close()

		#Using ffmpeg to convert the sampling rate to 16k
		os.system(f"ffmpeg -i {WAVE_OUTPUT_FILE} -ac 1 -ar 16000 -b:a 320000 -y {TEMP_OUTPUT_FILE}")
		os.system(f"mv {TEMP_OUTPUT_FILE} {WAVE_OUTPUT_FILE}")


	def record(self):
#		recorder = pyaudio.PyAudio()
		stream = self.recorder.open(format=pyaudio.paInt16,
							   channels=MAX_INPUT_CHANNELS,
							   rate=DEFAULT_SAMPLE_RATE,
							   input=True,
							   frames_per_buffer=CHUNKSIZE,
							   input_device_index=INPUT_DEVICE)
		frames=[]
		for i in range(0, int(DEFAULT_SAMPLE_RATE / CHUNKSIZE * DURATION)):
		#while not self.stop_audio:
			data = stream.read(CHUNKSIZE)
			frames.append(data)

		stream.stop_stream()
		stream.close()
		self.recorder.terminate()
		self.save_recording(frames)

	def stop(self):
		self.stop_audio=1


def get_device_info():
	recorder = pyaudio.PyAudio()
	num_devices = recorder.get_device_count()
	keys = ['name', 'index', 'maxInputChannels', 'defaultSampleRate']
	out_text=[]
	for n in range(num_devices):
		info_dict = recorder.get_device_info_by_index(n)
		values = [value for _,value in info_dict.items() if _ in keys]
		out = "\n".join([" : ".join([key,str(val)]) for key, val in zip(keys, values)])
		out_text.append(out)
	return "\n\n".join(out_text)


def main():
	st.set_page_config(layout="wide")
	title="Speech to Sign-Language."
	st.title(title)
	header="ASR speech to text demo."
	st.header(header)

	st.subheader("Display the working audio ports in your device to record audio.")
	device_text = ""
	if st.button("Get Device Audio Ports Info"):
		device_text=get_device_info()
		st.text(device_text)

	audio_recorder = record_audio()
	st.subheader("Record audio for prediction.")
	if st.button("Record"):
		with st.spinner(f"Recording."):
			audio_recorder.record()
			st.success("Recording done. Let's hear the recording.")
#	if st.button("Stop"):
#			audio.recorder.stop()
	# if text=="Sucess":

	st.subheader("Play the recorded audio.")
	if st.button("Play"):
		try:
			audio_file = open(WAVE_OUTPUT_FILE,"rb")
			audio_bytes = audio_file.read()
			st.audio(audio_bytes, format="audio/wav")
			audio_file.close()
		except:
			st.write("Please record sound first")

	st.subheader("Predictions")
	if st.button("Convert Speech to Text and detect Emotion"):
		col1, col2, col3 = st.beta_columns(3)

		col1.header("Predicted Text")
		col1.write("Under Construction")

		col2.header("Predicted Emotion")
		col2.write("Under Construction")

		col3.header("Sign Language Video")
		col3.write("Under Construction")


if __name__=="__main__":
	main()
