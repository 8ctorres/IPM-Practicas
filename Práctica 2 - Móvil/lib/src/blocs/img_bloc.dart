import 'dart:async';
import 'dart:io';

import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:iagram/src/resources/ApiRepository.dart';
import 'package:iagram/src/models/imgresponse.dart';

part 'img_event.dart';
part 'img_state.dart';

class ImgBloc extends Bloc<ImgEvent, ImgState> {
  final ApiRepository _apiRepository = ApiRepository();

  ImgBloc() : super(ImgInitialState());

  ImgState get initialState => ImgInitialState();

  @override
  Stream<ImgState> mapEventToState(
    ImgEvent event,
  ) async* {
    if (event is GetTags) {
      try {
        yield ImgLoadingState();
        final mList = await _apiRepository.getTags(event._image);
        yield ImgLoadedState(mList);
        if (mList.status.type != "success") {
          yield ImgErrorState(mList.status.type);
        }
      } on NetworkError {
        yield ImgErrorState("Failed to connect to the server");
      }
    }
  }
}
