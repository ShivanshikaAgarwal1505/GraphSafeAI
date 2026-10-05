import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../models/search_location.dart';

import '../../../core/network/api_client.dart';

class SearchService {
  static const String recentSearchesKey =
      'recent_searches';
 
  Future<List<SearchLocation>>
      loadPopularPlaces() async {
    final raw =
        await rootBundle.loadString(
      'assets/data/popular_places.json',
    );

    final List<dynamic> data =
        jsonDecode(raw);

    return data
        .map(
          (e) => SearchLocation.fromJson(
            e,
          ),
        )
        .toList();
  }

  Future<List<SearchLocation>>
      getRecentSearches() async {
    final prefs =
        await SharedPreferences.getInstance();

    final stored =
        prefs.getStringList(
              recentSearchesKey,
            ) ??
            [];

    return stored
        .map(
          (e) => SearchLocation.fromJson(
            jsonDecode(e),
          ),
        )
        .toList();
  }

  Future<void> saveSearch(
    SearchLocation location,
  ) async {
    final prefs =
        await SharedPreferences.getInstance();

    final existing =
        prefs.getStringList(
              recentSearchesKey,
            ) ??
            [];

    existing.removeWhere((item) {
      final search =
          SearchLocation.fromJson(
        jsonDecode(item),
      );

      return search.name ==
          location.name;
    });

    existing.insert(
      0,
      jsonEncode(
        location.toJson(),
      ),
    );

    await prefs.setStringList(
      recentSearchesKey,
      existing.take(10).toList(),
    );
  }

  Future<List<SearchLocation>>
      searchLocations(
    String query,
  ) async {
    final response =
        await ApiClient.dio.get(
      '/api/v1/navigation/search',
      queryParameters: {
        'q': query,
      },
    );

    final List data =
        response.data;

    return data
        .map(
          (e) =>
              SearchLocation.fromJson(e),
        )
        .toList();
  }
}