import 'package:flutter/material.dart';

import '../models/search_location.dart';
import '../services/search_service.dart';

class SearchProvider
    extends ChangeNotifier {
  final SearchService _service =
      SearchService();

  SearchLocation? selectedSource;

  SearchLocation? selectedDestination;

  List<SearchLocation> favoritePlaces = [];

  List<SearchLocation> recentSearches =
      [];

  List<SearchLocation> popularPlaces =
      [];

  List<SearchLocation> filteredResults =
      [];

  Future<void> initialize() async {
    popularPlaces =
        await _service.loadPopularPlaces();

    recentSearches =
        await _service.getRecentSearches();

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
  void search(String query) {
    if (query.trim().isEmpty) {
      filteredResults = [];
      notifyListeners();
      return;
    }

    filteredResults =
        popularPlaces.where((place) {
      return place.name
          .toLowerCase()
          .contains(
            query.toLowerCase(),
          );
    }).toList();

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
}