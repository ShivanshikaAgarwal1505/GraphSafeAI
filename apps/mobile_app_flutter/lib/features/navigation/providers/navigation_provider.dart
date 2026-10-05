import 'package:flutter/material.dart';

import '../models/route_response.dart';
import '../models/travel_mode.dart';
import '../models/route_preference.dart';
import '../services/navigation_service.dart';
 
class NavigationProvider extends ChangeNotifier {
  final NavigationService _service =
      NavigationService();

  bool loading = false;

  String? error;

  double sourceLat = 13.0827;
  double sourceLon = 80.2707;

  RouteResponse? safeRoute;
  RouteResponse? balancedRoute;
  RouteResponse? fastestRoute;

  TravelMode selectedTravelMode =
      TravelMode.walking;

  RoutePreference selectedRoute =
      RoutePreference.balanced;

  void setCurrentLocation({
    required double latitude,
    required double longitude,
  }) {
    sourceLat = latitude;
    sourceLon = longitude;

    notifyListeners();
  }

  RouteResponse? get activeRoute {
    switch (selectedRoute) {
      case RoutePreference.safe:
        return safeRoute;

      case RoutePreference.balanced:
        return balancedRoute;

      case RoutePreference.fastest:
        return fastestRoute;
    }
  }

  Future<void> loadRoutes({
    required double sourceLat,
    required double sourceLon,
    required double destinationLat,
    required double destinationLon,
  }) async {
    loading = true;
    error = null;

    notifyListeners();

    try {
      final mode =
          selectedTravelMode.name;

      final results = await Future.wait([
        _service.getRoute(
          profile: '${mode}_safe',
          sourceLat: sourceLat,
          sourceLon: sourceLon,
          destinationLat: destinationLat,
          destinationLon: destinationLon,
        ),
        _service.getRoute(
          profile: '${mode}_balanced',
          sourceLat: sourceLat,
          sourceLon: sourceLon,
          destinationLat: destinationLat,
          destinationLon: destinationLon,
        ),
        _service.getRoute(
          profile: '${mode}_fastest',
          sourceLat: sourceLat,
          sourceLon: sourceLon,
          destinationLat: destinationLat,
          destinationLon: destinationLon,
        ),
      ]);

      safeRoute = results[0];
      balancedRoute = results[1];
      fastestRoute = results[2];

      debugPrint(
  'SAFE NODES = ${safeRoute?.routeLength}',
);

debugPrint(
  'BALANCED NODES = ${balancedRoute?.routeLength}',
);

debugPrint(
  'FASTEST NODES = ${fastestRoute?.routeLength}',
);

debugPrint(
  'SAFE PROFILE = ${safeRoute?.profile}',
);

debugPrint(
  'BALANCED PROFILE = ${balancedRoute?.profile}',
);

debugPrint(
  'FASTEST PROFILE = ${fastestRoute?.profile}',
);
      selectedRoute =
          RoutePreference.balanced;
    } catch (e) {
      error = e.toString();
    } finally {
      loading = false;
      notifyListeners();
    }
  }

  void selectRoute(
    RoutePreference preference,
  ) {
    selectedRoute = preference;

    notifyListeners();
  }

  Future<void> toggleTravelMode({
    required double destinationLat,
    required double destinationLon,
  }) async {

    debugPrint(
      'MODE SWITCHED TO ${selectedTravelMode.name}',
    );

    selectedTravelMode =
        selectedTravelMode ==
                TravelMode.walking
            ? TravelMode.driving
            : TravelMode.walking;

    await loadRoutes(
      sourceLat: sourceLat,
      sourceLon: sourceLon,
      destinationLat: destinationLat,
      destinationLon: destinationLon,
    );
  }
}