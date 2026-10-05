import '../../../core/network/api_client.dart';
import '../models/search_location.dart';

class FavoriteService {

  Future<List<SearchLocation>>
      loadFavorites() async {

    final response =
        await ApiClient.dio.get(
      '/api/v1/favorites',
    );

    final List data =
        response.data;

    return data.map(
      (e) => SearchLocation(
        name: e['label'],
        latitude: e['latitude'],
        longitude: e['longitude'],
      ),
    ).toList();
  }

  Future<void> addFavorite({
    required String label,
    required double latitude,
    required double longitude,
  }) async {

    await ApiClient.dio.post(
      '/api/v1/favorites',
      data: {
        'label': label,
        'latitude': latitude,
        'longitude': longitude,
      },
    );
  }

  Future<void> removeFavorite(
    String label,
  ) async {

    final response =
        await ApiClient.dio.get(
      '/api/v1/favorites',
    );

    final List data =
        response.data;

    final favorite =
        data.firstWhere(
      (e) =>
          e['label'] ==
          label,
    );

    await ApiClient.dio.delete(
      '/api/v1/favorites/${favorite['id']}',
    );
  }
}