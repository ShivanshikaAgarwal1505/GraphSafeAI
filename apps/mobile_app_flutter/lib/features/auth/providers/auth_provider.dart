import 'package:flutter/material.dart';

import '../models/user_model.dart';
import '../services/auth_service.dart';

class AuthProvider extends ChangeNotifier {
  final AuthService _service = AuthService();

  UserModel? _user;

  bool _loading = false;

  UserModel? get user => _user;

  bool get isLoggedIn => _user != null;

  bool get loading => _loading;

  Future<void> initialize() async {
    _user = await _service.getCurrentUser();

    notifyListeners();
  }

  Future<bool> login({
    required String email,
    required String password,
  }) async {
    try {
      _loading = true;

      notifyListeners();

      _user = await _service.login(
        email: email,
        password: password,
      );

      return true;
    } catch (_) {
      return false;
    } finally {
      _loading = false;

      notifyListeners();
    }
  }

  Future<bool> register({
  required String name,
  required String email,
  required String password,
  }) async {
    try {
      _loading = true;

      notifyListeners();

      await _service.register(
        name: name,
        email: email,
        password: password,
      );

      _user = await _service.login(
        email: email,
        password: password,
      );

      return true;
    } catch (_) {
      return false;
    } finally {
      _loading = false;

      notifyListeners();
    }
  }

  Future<void> logout() async {
    await _service.logout();

    _user = null;

    notifyListeners();
  }
}