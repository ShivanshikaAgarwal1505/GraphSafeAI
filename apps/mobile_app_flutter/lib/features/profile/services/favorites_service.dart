import '../../../core/network/api_client.dart';

import '../models/favorite_location.dart';
import '../../../core/network/api_client.dart';

class FavoritesService {

  Future<List<FavoriteLocation>>
      loadFavorites() async {

    final response =
        await ApiClient.dio.get(
      '/api/v1/favorites',
    );

    final List data =
        response.data;

    return data
        .map(
          (e) =>
              FavoriteLocation
                  .fromJson(e),
        )
        .toList();
  }

  Future<void> deleteFavorite(
    int favoriteId,
  ) async {

    await ApiClient.dio.delete(
      '/api/v1/favorites/$favoriteId',
    );
  }

  Future<void> updateFavorite({
    required int id,
    required String label,
  }) async {

    await ApiClient.dio.put(
      '/api/v1/favorites/$id',
      data: {
        'label': label,
      },
    );
  }
}
