import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';

import '../services/location_service.dart';

class LocationProvider
    extends ChangeNotifier {

  final LocationService _service =
      LocationService();

  Position? position;

  bool loading = false;

  Future<void> loadLocation() async {

    loading = true;

    notifyListeners();

    try {

      position =
          await _service
              .getCurrentLocation();

    } finally {

      loading = false;

      notifyListeners();
    }
  }
}