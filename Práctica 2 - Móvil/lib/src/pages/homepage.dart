import 'dart:io';

import 'package:audioplayers/audio_cache.dart';
import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:iagram/src/blocs/img_bloc.dart';
import 'package:image_picker/image_picker.dart';

class HomePage extends StatefulWidget {
  static const routeName = "/";

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  File _image;
  final picker = ImagePicker();

  @override
  Widget build(BuildContext context) {
    return BlocListener<ImgBloc, ImgState>(
      listener: (context, state) {
        if ((state is ImgLoadingState) || (state is ImgLoadedState)){
          Navigator.of(context).pushNamed("/ResultsPage");
        }
      },
      child: Scaffold(
        appBar: AppBar(
          title: Text('IA gram'),
        ),
        body: Center(
          child: Text(
            'Pulsa el botón para escoger una foto',
            style: Theme.of(context).textTheme.headline6,
          ),
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: (){
            _showPicker();
          },
          tooltip: 'Escoger foto',
          child: Icon(Icons.add_a_photo),
        ),
      ),
    );
  }

  void _showPicker() {
    showModalBottomSheet(
        context: context,
        builder: (BuildContext bc) {
          return SafeArea(
            child: Container(
              child: new Wrap(
                children: <Widget>[
                  new ListTile(
                      leading: new Icon(Icons.photo_library),
                      title: new Text('Galería'),
                      onTap: () {
                        getFromGallery();
                        Navigator.of(context).pop();
                      }),
                  new ListTile(
                    leading: new Icon(Icons.photo_camera),
                    title: new Text('Cámara'),
                    onTap: () {
                      getFromCamera();
                      Navigator.of(context).pop();
                    },
                  ),
                ],
              ),
            ),
          );
        }
    );
  }

  Future getFromGallery() async {
    try {
      final pickedFile = await picker.getImage(source: ImageSource.gallery);

      setState(() {
        if (pickedFile != null) {
          _image = File(pickedFile.path);

          //Call the bloc and send the image
          BlocProvider.of<ImgBloc>(context).add(GetTags(_image));
        } else {
          print('ERROR: No image selected.');
        }
      });
    }
    catch (e){
      _showErrorDialog('No se ha podido acceder a la galería');
    }
  }

  Future getFromCamera() async {
    final pickedFile = await picker.getImage(source: ImageSource.camera);

    setState(() {
      if (pickedFile != null) {
        _image = File(pickedFile.path);

        //Call the bloc and send the image
        BlocProvider.of<ImgBloc>(context).add(GetTags(_image));
      } else {
        print('ERROR: No image selected.');
      }
    });
  }

  void _showErrorDialog(String errorMsg) {
    final player = AudioCache(prefix: 'assets/audios/');
    player.play('error.wav');
    showDialog(
      context: context,
      builder: (BuildContext context) {
        // return object of type Dialog
        return AlertDialog(
          title: new Text("Error"),
          content: new Text(errorMsg),
          actions: <Widget>[
            // usually buttons at the bottom of the dialog
            new FlatButton(
              child: new Text("Close"),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }
}
