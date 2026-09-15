import '../../navigation/models/route_response.dart';
import '../../../core/network/api_client.dart';

class NavigationService {
  Future<RouteResponse> getRoute({
    required String profile,
    required double sourceLat,
    required double sourceLon,
    required double destinationLat,
    required double destinationLon,
  }) async {
    final response = await ApiClient.dio.get(
      '/api/v1/navigation/route',
      queryParameters: {
        'source_lat': sourceLat,
        'source_lon': sourceLon,
        'destination_lat': destinationLat,
        'destination_lon': destinationLon,
        'profile': profile,
      },
    );

    return RouteResponse.fromJson(response.data);
  }
}