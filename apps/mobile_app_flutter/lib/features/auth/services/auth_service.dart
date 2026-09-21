import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../../../core/network/api_client.dart';
import '../models/user_model.dart';

class AuthService {
  final storage =
      const FlutterSecureStorage();

  Future<UserModel> login({
    required String email,
    required String password,
  }) async {
    final response =
        await ApiClient.dio.post(
      '/api/v1/auth/login',
      data: {
        'email': email,
        'password': password,
      },
    );

    await storage.write(
      key: 'access_token',
      value:
          response.data['access_token'],
    );

    return UserModel.fromJson(
      response.data['user'],
    );
  }

  Future<UserModel> register({
    required String name,
    required String email,
    required String password,
  }) async {
    final response =
        await ApiClient.dio.post(
      '/api/v1/auth/register',
      data: {
        'name': name,
        'email': email,
        'password': password,
      },
    );

    return UserModel.fromJson(
      response.data,
    );
  }

  Future<UserModel?> getCurrentUser()
      async {
    try {
      final response =
          await ApiClient.dio.get(
        '/api/v1/auth/me',
      );

      return UserModel.fromJson(
        response.data,
      );
    } catch (_) {
      return null;
    }
  }

  Future<void> logout() async {
    await storage.delete(
      key: 'access_token',
    );
  }
}