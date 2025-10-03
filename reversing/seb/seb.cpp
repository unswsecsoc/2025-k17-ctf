#include <string>
#include <iostream>
#include <filesystem>
#include <algorithm>
#include <unistd.h>
#include <vector>
#include <sstream>
#include <string>
#include <set>
namespace fs = std::filesystem;

#include "instr.h"

// std::string encode_flag(std::string flag) {
//     auto state = uint32_t{2305847};
//     auto chars = std::vector<char>{flag.begin(), flag.end()};
//     chars.push_back(42);
//     auto new_chars = std::vector<char>{};
//     for (size_t i = 0; i < chars.size() - 1; i++) {
//         tf(state);
//         new_chars.push_back(chars[i] ^ chars[i + 1] ^ state);
//         new_chars.push_back(static_cast<char>(state * state));
//     }

//     std::stringstream ss;
//     // ss << std::hex;

//     for (size_t i{0}; i < new_chars.size(); ++i) {
//         // ss << std::setw(2) << std::setfill('0') << (int)new_chars[i];
//         ss << (int)new_chars[i] << ", ";
//     }

//     return ss.str();
//     return {new_chars.begin(), new_chars.end()};
// }

int op() {
    std::string path = "/proc";
    std::set<int> procs{};
    for (const auto &entry : fs::directory_iterator(path)) {
        auto name = entry.path().filename().string();
        if (name.find_first_not_of("0123456789") == name.npos) {
            procs.insert(std::stoi(name));
        }
    }

    if (procs != std::set<int>{1, getpid()}) {
        std::cout << "ERR: another process is running!" << std::endl;
        exit(1);
        return 0;
    }

    return 1;
}

namespace {
    int tf(uint32_t &x) {
        OBF_BEGIN
        V(x) ^= V(x) << N(18);
        V(x) ^= V(x) >> N(25);
        V(x) ^= V(x) << N(21);

        RETURN(0);
        OBF_END
    }

    __attribute__((noinline)) std::string decode_flag(const std::string& flag) {
        OBF_BEGIN
        std::vector<char> encoded_chars{flag.begin(), flag.end()};

        size_t num_pairs = encoded_chars.size() / N(2);
        size_t original_size = V(num_pairs) + N(1);

        std::vector<char> decoded_chars(V(original_size));

        decoded_chars[V(original_size) - N(1)] = N(42);

        uint32_t state = N(2305847);
        std::vector<char> states;
        size_t i = 0;
        FOR (V(i) = N(0), V(i) < V(num_pairs), V(i)++)
            tf(state);
            states.push_back(V(state));
        ENDFOR

        ssize_t j;
        FOR (V(j) = V(original_size) - N(2), V(j) >= N(0L), V(j) -= 2)
            char xor_char = encoded_chars[(V(j) << N(11)) >> N(10)];
            V(j) += N(1);
            IF (op())
                decoded_chars[V(j) - N(1)] = decoded_chars[V(j)] ^ V(xor_char) ^ states[V(j) - N(1)];
            ENDIF
        ENDFOR

        decoded_chars.pop_back();

        RETURN(std::string(decoded_chars.begin(), decoded_chars.end()));

        OBF_END
    }

    std::string enc_p = {19, 17, 25, -63, 10, 36, 39, -7, 93, -71, 42, 73, 73, 16, 51, -47, 122, 17, 9, -63, 125, 36, 30, -7, 119, -71, 20, 73, 81, 16, 28, -47, 95, 17, 2, -63, 21, 36, 97, -7, 71, -71, 43, 73, 64, 16, 42, -47, 118, 17, 3, -63, 70, 36, 47, -7, 96, -71, 19, 73, 77, 16, 13, -47, 66, 17, 4, -63, 118, 36, 24, -7, 124, -71, 39, 73, 120, 16, 127, -47, 105, 17, 21, -63, 26, 36, 98, -7};
}

int main() {
    // std::cout << encode_flag("K17{i_heard_that_it's_impossible_to_re_c++!}");

    std::cout << "Welcome to Secure Exam Browser\n" << "Enter Password: ";
    std::string pass{};
    std::cin >> pass;
    auto flag = decode_flag(enc_p);
    if (pass == flag) {
        std::cout << "Integrity check complete!\n";
        std::cout << "No exams available. Exiting.\n";
    } else {
        std::cout << "Incorrect password!\n";
    }
}
