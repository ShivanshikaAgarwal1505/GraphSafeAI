import 'package:flutter/material.dart';

import '../models/search_location.dart';
import '../services/search_service.dart';
import '../services/favorite_service.dart';

class SearchProvider
    extends ChangeNotifier {
  final SearchService _service =
      SearchService();
  
  final FavoriteService
    _favoriteService =
        FavoriteService();

  SearchLocation? selectedSource;

  SearchLocation? selectedDestination;

  List<SearchLocation> favoritePlaces = [];

  List<SearchLocation> recentSearches =
      [];

  List<SearchLocation> popularPlaces =
      [];

  List<SearchLocation> filteredResults =
      [];

  bool isFavorite(
    SearchLocation location,
  ) {
    return favoritePlaces.any(
      (f) =>
          f.name == location.name,
    );
  }

  Future<void> initialize() async {
    popularPlaces =
        await _service.loadPopularPlaces();

    recentSearches =
        await _service.getRecentSearches();

    favoritePlaces =
    await _favoriteService
        .loadFavorites();

    notifyListeners();
  }

  void setSource(
    SearchLocation location,
  ) {
    selectedSource = location;
    notifyListeners();
  }

  void swapLocations() {
    final temp =
        selectedSource;

    selectedSource =
        selectedDestination;

    selectedDestination =
        temp;

    notifyListeners();
  }

  Future<void> search(
    String query,
  ) async {
    if (query.trim().isEmpty) {
      filteredResults = [];
      notifyListeners();
      return;
    }

    filteredResults =
        await _service
            .searchLocations(
      query,
    );

    notifyListeners();
  }

  Future<void> setDestination(
    SearchLocation location,
  ) async {
    debugPrint(
      'setDestination called: ${location.name}',
    );
    selectedDestination = location;

    debugPrint(
      'selectedDestination assigned',
    );
    await _service.saveSearch(
      location,
    );

    recentSearches =
        await _service.getRecentSearches();

    notifyListeners();
  }

  void clearDestination() {
    selectedDestination = null;

    notifyListeners();
  }

  Future<void> addFavorite(
    SearchLocation location,
  ) async {

    await _favoriteService.addFavorite(
      label: location.name,
      latitude: location.latitude,
      longitude: location.longitude,
    );

    favoritePlaces =
        await _favoriteService
            .loadFavorites();

    notifyListeners();
  }

  Future<void> toggleFavorite(
    SearchLocation location,
  ) async {

    if (
        isFavorite(
          location,
        )) {

      await _favoriteService
          .removeFavorite(
        location.name,
      );

    } else {

      await _favoriteService
          .addFavorite(
        label:
            location.name,
        latitude:
            location.latitude,
        longitude:
            location.longitude,
      );
    }

    favoritePlaces =
        await _favoriteService
            .loadFavorites();

    notifyListeners();
  }
}