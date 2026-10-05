import 'package:flutter/material.dart';

import '../models/favorite_location.dart';
import '../services/favorites_service.dart';

class FavoritesScreen
    extends StatefulWidget {

  const FavoritesScreen({
    super.key,
  });

  @override
  State<FavoritesScreen>
      createState() =>
          _FavoritesScreenState();
}

class _FavoritesScreenState
    extends State<FavoritesScreen> {

  final service =
      FavoritesService();

  List<FavoriteLocation>
      favorites = [];

  bool loading = true;

  @override
  void initState() {
    super.initState();

    loadFavorites();
  }

  Future<void> loadFavorites()
  async {

    favorites =
        await service
            .loadFavorites();

    setState(() {
      loading = false;
    });
  }

  Future<void>
      deleteFavorite(
    FavoriteLocation
        favorite,
  ) async {

    await service
        .deleteFavorite(
      favorite.id,
    );

    await loadFavorites();
  }

  Future<void> renameFavorite(
    FavoriteLocation favorite,
  ) async {

    final controller =
        TextEditingController(
      text: favorite.label,
    );

    final result =
        await showDialog<String>(
      context: context,
      builder: (_) {
        return AlertDialog(
          title: const Text(
            'Rename Favorite',
          ),

          content: TextField(
            controller: controller,
            decoration:
                const InputDecoration(
              hintText:
                  'Favorite Name',
            ),
          ),

          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(
                  context,
                );
              },
              child:
                  const Text(
                'Cancel',
              ),
            ),

            FilledButton(
              onPressed: () {
                Navigator.pop(
                  context,
                  controller.text,
                );
              },
              child:
                  const Text(
                'Save',
              ),
            ),
          ],
        );
      },
    );

    if (result == null ||
        result.trim().isEmpty) {
      return;
    }

    await service.updateFavorite(
      id: favorite.id,
      label: result,
    );

    await loadFavorites();
  }

  // Future<void> updateFavorite({
  //   required int id,
  //   required String label,
  // }) async {

  //   await ApiClient.dio.put(
  //     '/api/v1/favorites/$id',
  //     data: {
  //       'label': label,
  //     },
  //   );
  // }

  @override
  Widget build(
    BuildContext context,
  ) {

    return Scaffold(
      appBar: AppBar(
        title:
            const Text(
          'Favorites',
        ),
      ),

      body: loading
          ? const Center(
              child:
                  CircularProgressIndicator(),
            )
          : favorites.isEmpty
              ? const Center(
                  child: Text(
                    'No favorites added yet',
                  ),
                )
              : ListView.builder(
                  itemCount:
                      favorites
                          .length,
                  itemBuilder:
                      (
                    context,
                    index,
                  ) {
                    final favorite =
                        favorites[
                            index];

                    return ListTile(
                      leading: const Icon(
                        Icons.star,
                        color: Colors.amber,
                      ),

                      title: Text(
                        favorite.label,
                      ),

                      subtitle: Text(
                        '${favorite.latitude.toStringAsFixed(4)}, '
                        '${favorite.longitude.toStringAsFixed(4)}',
                      ),

                      trailing: PopupMenuButton<String>(
                        itemBuilder: (_) => [
                          const PopupMenuItem(
                            value: 'rename',
                            child: Text(
                              'Rename',
                            ),
                          ),
                          const PopupMenuItem(
                            value: 'delete',
                            child: Text(
                              'Delete',
                            ),
                          ),
                        ],

                        onSelected: (
                          value,
                        ) async {

                          if (value ==
                              'rename') {

                            await renameFavorite(
                              favorite,
                            );
                          }

                          if (value ==
                              'delete') {

                            await deleteFavorite(
                              favorite,
                            );
                          }
                        },
                      ),
                    );
                  },
                ),
    );
  }
}