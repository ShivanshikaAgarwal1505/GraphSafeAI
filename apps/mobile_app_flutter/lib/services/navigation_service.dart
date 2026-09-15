import 'package:dio/dio.dart';

import '../core/network/api_client.dart';
import '../core/constants/api_constants.dart';

class NavigationService {

  Future<Response> getRoute(
      String profile) {

    return ApiClient.dio.get(
      ApiConstants.routeEndpoint,
      queryParameters: {

        'source_lat': 13.0520,
        'source_lon': 80.2020,

        'destination_lat': 13.0370,
        'destination_lon': 80.1620,

        'profile': profile,
      },
    );
  }
}