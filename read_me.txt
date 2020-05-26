Project opens up a GUI built using Tkinter,
where it takes snapshot of the image coming in front of webcam.
Recognises face from it using XML file.
Then sends it into ML model to classify it.
Uses voice search method.

"""IMPORTANT""""
For better performance
while creating dataset, extract only the face from image used using XML file provided.
and convert the extracted face in Black and White.


Shortcommings
Works for dataset of two people only
If a third person comes, will fail
Also during first step when taking the SS, if it see's multiple faces it crashes
