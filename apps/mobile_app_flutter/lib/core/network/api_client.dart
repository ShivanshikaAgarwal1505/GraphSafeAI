import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../constants/api_constants.dart';
 
class ApiClient {
  static final FlutterSecureStorage _storage =
      const FlutterSecureStorage();

  static final Dio dio = Dio(
    BaseOptions(
      baseUrl: ApiConstants.baseUrl,
      connectTimeout: const Duration(
        seconds: 20,
      ),
      receiveTimeout: const Duration(
        seconds: 20,
      ),
    ),
  )
    ..interceptors.add(
      InterceptorsWrapper(
        onRequest: (
          options,
          handler,
        ) async {
          final token =
              await _storage.read(
            key: 'access_token',
          );

          if (token != null) {
            options.headers[
                'Authorization'] =
                'Bearer $token';
          }

          handler.next(options);
        },
      ),
    );
}