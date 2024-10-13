#include <stdio.h>
#include <fstream>
#include <set>
#include <iostream>
#include <cstdint>
#include <cmath>
#include <algorithm>
#include <numeric>

uint16_t swapEndianUint16(uint16_t value) {
    return ((value & 0x00FF) << 8) |
           ((value & 0xFF00) >> 8);
}

uint32_t swapEndianUint32(uint32_t value) {
    return ((value & 0x000000FF) << 24) |
           ((value & 0x0000FF00) << 8) |
           ((value & 0x00FF0000) >> 8) |
           ((value & 0xFF000000) >> 24);
}

int16_t read_int16(std::ifstream &file, long offset) {
    file.seekg(offset, std::ios::beg);
    uint32_t hdr;
    file.read(reinterpret_cast<char*>(&hdr), 2);
    return swapEndianUint16(hdr);
}

uint16_t read_uint16(std::ifstream &file, long offset) {
    file.seekg(offset, std::ios::beg);
    uint32_t hdr;
    file.read(reinterpret_cast<char*>(&hdr), 2);
    return swapEndianUint16(hdr);
}

uint32_t read_uint32(std::ifstream &file, long offset) {
    file.seekg(offset, std::ios::beg);
    uint32_t hdr;
    file.read(reinterpret_cast<char*>(&hdr), 4);
    return swapEndianUint32(hdr);
}

int main(int argc, char* argv[]) {
    std::string segy_filename = "npr3_gathers.sgy";
    std::ifstream file(segy_filename, std::ios::binary | std::ios::ate);

    std::cout << "Чтение заголовков С++" << std::endl;

    if (!file.is_open()) {
        std::cerr << "Failed to open file: " << segy_filename << std::endl;
        return -1;
    }

    // Get the file size
    std::streamsize fileSize = file.tellg();
    
    uint16_t num_samples = read_uint16(file, 3220);
    
    std::streamsize traceSize = num_samples * sizeof(float) + 240;
    int numberOfTraces = (fileSize - 3600) / traceSize;    

    std::set<int> cdps;
    std::set<float> cdps_z;

    float mult = 1.0;
    uint32_t hdr;

    for (int i = 0; i < numberOfTraces; ++i) {
        // Seek to the trace samples offset
        long offset = 3600 + i * traceSize;
        
        if (i == 0) {
            int16_t coef = read_int16(file, offset + 68);            
            mult = std::pow(std::abs(coef), std::copysign(1.0, coef));            
        }
    
        hdr = read_uint32(file, offset + 20);
        if (cdps.find(hdr) == cdps.end()) { 
            cdps.insert(hdr);
            hdr = read_uint32(file, offset + 40);
            float rec_z = hdr * mult;
            hdr = read_uint32(file, offset + 44);
            float sou_z = hdr * mult;
            cdps_z.insert((rec_z + sou_z) / 2);
        }
    }
    file.close();

    int min_cdp = *cdps.begin();
    int max_cdp = *cdps.rbegin();
    float min_cdp_z = *cdps_z.begin();
    float max_cdp_z = *cdps_z.rbegin();
    double sum = std::accumulate(cdps_z.begin(), cdps_z.end(), 0.0f);
    double mean_cdp_z = sum / cdps_z.size();

    std::cout << "CDP: мин = " << min_cdp << ", макс = " << max_cdp << ", всего уникальных: " << cdps.size() << std::endl;
    std::cout << "CDP_ELEV: мин = " << min_cdp_z << ", макс = " << max_cdp_z << ", среднее = " << mean_cdp_z << std::endl;
    
    return 0;
}