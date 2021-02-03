part of 'img_bloc.dart';

abstract class ImgState extends Equatable {
  const ImgState();
}

class ImgInitialState extends ImgState {
  const ImgInitialState();
  @override
  List<Object> get props => [];
}

class ImgLoadingState extends ImgState {
  const ImgLoadingState();
  @override
  List<Object> get props => [];
}

class ImgLoadedState extends ImgState {
  final ResponseModel responseModel;
  const ImgLoadedState(this.responseModel);
  @override
  List<Object> get props => [];
}

class ImgErrorState extends ImgState {
  final String errorMsg;
  const ImgErrorState(this.errorMsg);
  @override
  List<Object> get props => [];
}
