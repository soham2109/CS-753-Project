## CS-753 Project Abstract

1. Project Abstract

	With the aim of converting speech to sign-language for the hearing-impaired, we first convert the speech to text and then from text to sign-language. In addition to this we also would like to extract the emotion conveyed by the speech signal and display it to them as well because the sign language itself by the hand does not convey any sort of emotion.  
	For this we would first try to train two different networks. The two networks are to train on the speech data, with one network converting the speech signal to text and the other detecting the emotion. Then, depending on the detected text we output the corresponding sign-language, along with the emotion conveyed with it.  

2. Datasets

	- For emotion detection network: RAVDESS speech dataset  
	- For speech to text network: Google Audioset  