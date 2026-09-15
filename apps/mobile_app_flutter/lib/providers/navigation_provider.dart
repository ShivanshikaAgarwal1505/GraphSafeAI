import 'package:flutter/material.dart';

import '../models/route_response.dart';
import '../services/navigation_service.dart';

class NavigationProvider extends ChangeNotifier {

  final NavigationService _service =
      NavigationService();

  bool loading = false;

  String selectedProfile =
      'walking_safe';

  RouteResponse? route;

  Future<void> loadRoute() async {

    loading = true;

    notifyListeners();

    try {

      final response =
          await _service.getRoute(
        selectedProfile,
      );

      route =
          RouteResponse.fromJson(
        response.data,
      );

    } finally {

      loading = false;

      notifyListeners();
    }
  }

  void selectProfile(
      String profile) {

    selectedProfile = profile;

    notifyListeners();
  }
}