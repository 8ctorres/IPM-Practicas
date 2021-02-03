import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:iagram/src/pages/homepage.dart';
import 'package:iagram/src/pages/resultspage.dart';

import 'blocs/img_bloc.dart';

class App extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => ImgBloc(),
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        routes: {
          "/": (context) => HomePage(),
          "/ResultsPage": (context) => ResultsPage(),
        },
        initialRoute: "/",
        theme: ThemeData(
          floatingActionButtonTheme: FloatingActionButtonThemeData(
            foregroundColor: Colors.white,
          ),
        ),
        darkTheme:
            ThemeData.dark(), //Makes app automatically adapt to the OSs Theme
      ),
    );
  }
}
