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


def save_recording(frames):
	if not frames:
		raise ValueError("No frames recorded.")
	recorder = pyaudio.PyAudio()
	wavfile = wave.open(WAVE_OUTPUT_FILE,"wb")
	wavfile.setnchannels(MAX_INPUT_CHANNELS)
	wavfile.setsampwidth(recorder.get_sample_size(pyaudio.paInt16))
	wavfile.setframerate(DEFAULT_SAMPLE_RATE)
	wavfile.writeframes(b''.join(frames))
	wavfile.close()

	#Using ffmpeg to convert the sampling rate to 16k
	os.system(f"ffmpeg -i {WAVE_OUTPUT_FILE} -ac 1 -ar 16000 -y {TEMP_OUTPUT_FILE}")
	os.system(f"mv {TEMP_OUTPUT_FILE} {WAVE_OUTPUT_FILE}")


def record():
	recorder = pyaudio.PyAudio()
	stream = recorder.open(format=pyaudio.paInt16,
						   channels=MAX_INPUT_CHANNELS,
						   rate=DEFAULT_SAMPLE_RATE,
						   input=True,
						   frames_per_buffer=CHUNKSIZE,
						   input_device_index=INPUT_DEVICE)
	frames=[]
	for i in range(0, int(DEFAULT_SAMPLE_RATE / CHUNKSIZE * DURATION)):
		data = stream.read(CHUNKSIZE)
		frames.append(data*10)

	stream.stop_stream()
	stream.close()
	recorder.terminate()
	save_recording(frames)


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
	title="Speech to Sign-Language."
	st.title(title)
	header="ASR speech to text demo."
	st.header(header)
	device_text = ""
	if st.button("Get Device Audio Ports Info"):
		device_text=get_device_info()
		st.write(device_text)

	if st.button("Record"):
		with st.spinner(f"Recording for {DURATION} seconds."):
			record()
			st.success("Recording done. Let's hear the recording.")
	# if text=="Sucess":


	if st.button("Play"):
		try:
			audio_file = open(WAVE_OUTPUT_FILE,"rb")
			audio_bytes = audio_file.read()
#			audio_placeholder = st.empty()
#			mymidia_str = "data:audio/wav;base64,%s"%(base64.b64encode(audio_bytes).decode())
#			mymidia_html = """
#				<audio autoplay class="stAudio">
#				<source src="%s" type="audio/wav">
#				Your browser does not support the audio element.
#				</audio>
#			"""%mymidia_str
#			time.sleep(1)
#			audio_placeholder.empty()
#			audio_placeholder.markdown(mymidia_html, unsafe_allow_html=True)
			st.audio(audio_bytes, format="audio/wav")
			audio_file.close()
		except:
			st.write("Please record sound first")

	if st.button("Convert Speech to Text"):
		st.write("Under construction.")

if __name__=="__main__":
	main()
