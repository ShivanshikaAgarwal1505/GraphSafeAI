import 'package:flutter/material.dart';

import '../models/route_response.dart';
import '../services/navigation_service.dart';

class NavigationProvider extends ChangeNotifier {
  final NavigationService _service = NavigationService();

  bool loading = false;

  String? error;

  String selectedProfile = 'walking_balanced';

  double sourceLat = 13.0827;
  double sourceLon = 80.2707;

  double destinationLat = 13.1324;
  double destinationLon = 80.2727;

  RouteResponse? route;

  void setCurrentLocation({
    required double latitude,
    required double longitude,
  }) {
    sourceLat = latitude;
    sourceLon = longitude;

    notifyListeners();
  }

  Future<void> loadRoute() async {
    loading = true;
    error = null;

    notifyListeners();

    try {
      route = await _service.getRoute(
        profile: selectedProfile,
        sourceLat: sourceLat,
        sourceLon: sourceLon,
        destinationLat: destinationLat,
        destinationLon: destinationLon,
      );
    } catch (e) {
      error = e.toString();
    } finally {
      loading = false;
      notifyListeners();
    }
  }
}