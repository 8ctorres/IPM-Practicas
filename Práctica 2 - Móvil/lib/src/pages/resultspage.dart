import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_device_type/flutter_device_type.dart';
import 'package:iagram/src/blocs/img_bloc.dart';
import 'package:iagram/src/models/imgresponse.dart';

class ResultsPage extends StatefulWidget {
  static const routeName = '/ResultsPage';
  @override
  State<StatefulWidget> createState() => _ResultsPageState();
}

class _ResultsPageState extends State<ResultsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("IA gram - Resultados"),
      ),
      body: BlocBuilder<ImgBloc, ImgState>(
        builder: (context, state) {
          if ((state is ImgInitialState) || (state is ImgLoadingState)) {
            return _buildLoading();
          } else if (state is ImgLoadedState) {
            return _buildTagCards(context, state.responseModel);
          } else {
            return Container();
          }
        },
      ),
    );
  }

  Widget _buildLoading() => Center(child: CircularProgressIndicator());

  Widget _buildTagCards(BuildContext context, ResponseModel model) {
    return OrientationBuilder(
      builder: (context, orientation){
        return CustomScrollView(
          slivers: [
            SliverPadding(
              padding: const EdgeInsets.all(16),
              sliver: SliverGrid(
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: _calculateColumns(orientation),
                  childAspectRatio: 3,
                ),
                delegate: SliverChildBuilderDelegate(
                    (context, index){
                      return _buildTagWidget(context, model.result.tags[index]);
                    },
                  childCount: model.result.tags.length,
                ),
              ),
            ),
          ],
        );
      },
    );
  }

  //Calculates the layout of the results based on device type and orientation
  int _calculateColumns(Orientation orientation) {
    if (Device.get().isTablet) {
      return orientation == Orientation.portrait ? 3 : 4;
    } else if (Device.get().isPhone) {
      return orientation == Orientation.portrait ? 1 : 2;
    } else
      return 1;
  }

  Widget _buildTagWidget(BuildContext context, TagItem tagItem) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.only(bottom: 4),
          alignment: Alignment.centerLeft,
          child: Text(
            tagItem.tag.es[0].toUpperCase() +
                tagItem.tag.es.substring(1).toLowerCase(),
            style: Theme.of(context).textTheme.headline6,
          ),
        ),
        Container(
          padding: const EdgeInsets.only(left: 4, bottom: 6),
          alignment: Alignment.centerLeft,
          child: Text(
            "(" +
                tagItem.tag.en[0].toUpperCase() +
                tagItem.tag.en.substring(1).toLowerCase() +
                ")",
            style: Theme.of(context).textTheme.subtitle2,
          ),
        ),
        Container(
          padding: const EdgeInsets.only(left: 4),
          alignment: Alignment.centerLeft,
          child: Text(
            "Confianza: " +
                tagItem.confidence.toString().substring(0, 5) +
                "%",
            style: Theme.of(context).textTheme.subtitle2,
          ),
        ),
      ],
    );
  }
}
