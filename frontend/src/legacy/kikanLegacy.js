export const kikanLegacy = `
/* ---------------- Data ---------------- */
const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const PREFS = {"hokkaido":{"name":"Hokkaido","archetype":"hokkaido","capital":"Sapporo","hazards":{"typhoon":31,"rain":34,"flood":20,"landslide":16,"thunder":24,"snow":72},"monthly":{"disruption":[62,55,30,18,14,20,28,34,40,30,45,68],"typhoon":[2,2,3,4,5,9,16,27,31,18,7,3],"flood":[10,10,15,20,22,28,32,34,30,22,16,12],"landslide":[6,6,10,14,18,22,26,28,24,16,10,8],"snow":[85,80,55,20,4,0,0,0,0,10,45,78]},"predicts":"Hokkaido's highest disruption from heavy snow between December and February, with a secondary rise in typhoon-linked rain during September.","shelters":[{"name":"Sapporo Civic Gymnasium","jp":"\\u672d\\u5e4c\\u5e02\\u6c11\\u4f53\\u80b2\\u9928","note":"English support, wheelchair access","loc":"Sapporo"},{"name":"Asahikawa Community Hall","jp":"\\u65ed\\u5ddd\\u30b3\\u30df\\u30e5\\u30cb\\u30c6\\u30a3\\u30db\\u30fc\\u30eb","note":"Pet-friendly area available","loc":"Asahikawa"},{"name":"Kushiro Riverside Center","jp":"\\u91e7\\u8def\\u30ea\\u30d0\\u30fc\\u30b5\\u30a4\\u30c9\\u30bb\\u30f3\\u30bf\\u30fc","note":"Elevated ground, flood-safe","loc":"Kushiro"}],"places":[{"name":"Sapporo Snow Festival Grounds","jp":"\\u3055\\u3063\\u307d\\u308d\\u96ea\\u307e\\u3064\\u308a\\u4f1a\\u5834","note":"Odori Park \\u2014 famous winter ice sculpture festival","loc":"Sapporo","nearest":"Sapporo Civic Gymnasium"},{"name":"Biei Blue Pond","jp":"\\u9752\\u3044\\u6c60","note":"Striking blue pond, especially in autumn","loc":"Biei","nearest":"Asahikawa Community Hall"},{"name":"Kushiro Marsh","jp":"\\u91e7\\u8def\\u6e7f\\u539f","note":"Japan's largest wetland, boardwalk trails","loc":"Kushiro","nearest":"Kushiro Riverside Center"}],"towns":["Asahikawa","Biei","Kushiro","Sapporo"],"typhoonGrade":"Typhoon","typhoonRealData":{"landfalls_2000_2025":10,"max_wind_kmh":101.9,"grade_counts":{"3":6,"4":4,"5":0}}},"aomori":{"name":"Aomori","archetype":"tohoku","capital":"Aomori","hazards":{"typhoon":19,"rain":38,"flood":26,"landslide":22,"thunder":26,"snow":58},"monthly":{"disruption":[48,42,30,22,20,32,42,38,36,26,32,50],"typhoon":[1,1,2,3,5,7,12,19,18,10,4,2],"flood":[12,12,16,20,26,36,40,34,28,20,16,14],"landslide":[8,8,12,16,22,30,34,28,22,16,12,10],"snow":[70,64,40,14,2,0,0,0,0,4,30,62]},"predicts":"Aomori's rising flood and landslide risk through June-July's rainy season, plus meaningful snow disruption December-February.","shelters":[{"name":"Aomori Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Aomori"}],"places":[{"name":"Aomori City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Aomori","nearest":"Aomori Community Shelter"}],"towns":["Aomori"],"typhoonGrade":"Typhoon","typhoonRealData":{"landfalls_2000_2025":6,"max_wind_kmh":111.1,"grade_counts":{"3":3,"4":3,"5":0}}},"iwate":{"name":"Iwate","archetype":"tohoku","capital":"Morioka","hazards":{"typhoon":6,"rain":38,"flood":26,"landslide":22,"thunder":26,"snow":58},"monthly":{"disruption":[48,42,30,22,20,32,42,38,36,26,32,50],"typhoon":[0,0,1,1,2,2,4,6,6,3,1,1],"flood":[12,12,16,20,26,36,40,34,28,20,16,14],"landslide":[8,8,12,16,22,30,34,28,22,16,12,10],"snow":[70,64,40,14,2,0,0,0,0,4,30,62]},"predicts":"Iwate's rising flood and landslide risk through June-July's rainy season, plus meaningful snow disruption December-February.","shelters":[{"name":"Morioka Community Center","jp":"\\u76db\\u5ca1\\u30b3\\u30df\\u30e5\\u30cb\\u30c6\\u30a3\\u30bb\\u30f3\\u30bf\\u30fc","note":"Tsunami-safe elevation","loc":"Morioka"}],"places":[{"name":"Lake Tazawa","jp":"\\u7530\\u6ca2\\u6e56","note":"Nearby deep, striking cobalt-blue lake","loc":"Morioka area","nearest":"Morioka Community Center"}],"towns":["Morioka","Morioka area"],"typhoonGrade":"Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":2,"max_wind_kmh":120.4,"grade_counts":{"3":0,"4":1,"5":1}}},"miyagi":{"name":"Miyagi","archetype":"tohoku","capital":"Sendai","hazards":{"typhoon":3,"rain":38,"flood":26,"landslide":22,"thunder":26,"snow":58},"monthly":{"disruption":[48,42,30,22,20,32,42,38,36,26,32,50],"typhoon":[0,0,0,0,1,1,2,3,3,2,1,0],"flood":[12,12,16,20,26,36,40,34,28,20,16,14],"landslide":[8,8,12,16,22,30,34,28,22,16,12,10],"snow":[70,64,40,14,2,0,0,0,0,4,30,62]},"predicts":"Miyagi's rising flood and landslide risk through June-July's rainy season, plus meaningful snow disruption December-February.","shelters":[{"name":"Sendai Evacuation Hub","jp":"\\u4ed9\\u53f0\\u907f\\u96e3\\u62e0\\u70b9","note":"English support, medical staff on site","loc":"Sendai"}],"places":[{"name":"Matsushima Bay","jp":"\\u677e\\u5cf6","note":"One of Japan's Three Great Views \\u2014 pine-covered islets","loc":"Matsushima","nearest":"Sendai Evacuation Hub"}],"towns":["Matsushima","Sendai"],"typhoonGrade":"Typhoon","typhoonRealData":{"landfalls_2000_2025":1,"max_wind_kmh":64.8,"grade_counts":{"3":1,"4":0,"5":0}}},"akita":{"name":"Akita","archetype":"tohoku","capital":"Akita","hazards":{"typhoon":3,"rain":38,"flood":26,"landslide":22,"thunder":26,"snow":55},"monthly":{"disruption":[48,42,30,22,20,32,42,38,36,26,32,50],"typhoon":[0,0,0,0,1,1,2,3,3,2,1,0],"flood":[12,12,16,20,26,36,40,34,28,20,16,14],"landslide":[8,8,12,16,22,30,34,28,22,16,12,10],"snow":[55,41,12,0,0,0,0,0,0,0,3,38]},"predicts":"Akita's rising flood and landslide risk through June-July's rainy season, plus meaningful snow disruption December-February.","shelters":[{"name":"Akita Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Akita"}],"places":[{"name":"Akita City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Akita","nearest":"Akita Community Shelter"}],"towns":["Akita"],"typhoonGrade":"Typhoon","typhoonRealData":{"landfalls_2000_2025":1,"max_wind_kmh":74.1,"grade_counts":{"3":1,"4":0,"5":0}},"snowRealData":{"source":"JMA station data, 2022\\u20132026 daily average, Akita/Yamagata"}},"yamagata":{"name":"Yamagata","archetype":"tohoku","capital":"Yamagata","hazards":{"typhoon":28,"rain":38,"flood":26,"landslide":22,"thunder":26,"snow":73},"monthly":{"disruption":[48,42,30,22,20,32,42,38,36,26,32,50],"typhoon":[2,2,3,5,8,12,20,32,30,16,6,3],"flood":[12,12,16,20,26,36,40,34,28,20,16,14],"landslide":[8,8,12,16,22,30,34,28,22,16,12,10],"snow":[73,54,20,2,0,0,0,0,0,0,2,47]},"predicts":"Yamagata's rising flood and landslide risk through June-July's rainy season, plus meaningful snow disruption December-February.","shelters":[{"name":"Yamagata Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Yamagata"}],"places":[{"name":"Yamagata City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Yamagata","nearest":"Yamagata Community Shelter"}],"towns":["Yamagata"],"typhoonGrade":null,"typhoonRealData":null,"snowRealData":{"source":"JMA station data, 2022\\u20132026 daily average, Akita/Yamagata"}},"fukushima":{"name":"Fukushima","archetype":"tohoku","capital":"Fukushima","hazards":{"typhoon":28,"rain":38,"flood":26,"landslide":22,"thunder":26,"snow":58},"monthly":{"disruption":[48,42,30,22,20,32,42,38,36,26,32,50],"typhoon":[2,2,3,5,8,12,20,32,30,16,6,3],"flood":[12,12,16,20,26,36,40,34,28,20,16,14],"landslide":[8,8,12,16,22,30,34,28,22,16,12,10],"snow":[70,64,40,14,2,0,0,0,0,4,30,62]},"predicts":"Fukushima's rising flood and landslide risk through June-July's rainy season, plus meaningful snow disruption December-February.","shelters":[{"name":"Fukushima Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Fukushima"}],"places":[{"name":"Fukushima City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Fukushima","nearest":"Fukushima Community Shelter"}],"towns":["Fukushima"],"typhoonGrade":null,"typhoonRealData":null},"ibaraki":{"name":"Ibaraki","archetype":"kanto","capital":"Mito","hazards":{"typhoon":44,"rain":36,"flood":24,"landslide":14,"thunder":32,"snow":8},"monthly":{"disruption":[20,18,22,24,28,40,36,50,58,42,24,20],"typhoon":[1,1,2,4,8,14,20,42,50,28,6,2],"flood":[10,10,14,18,24,38,34,32,30,22,14,10],"landslide":[4,4,6,8,12,20,22,18,16,10,6,5],"snow":[10,12,4,0,0,0,0,0,0,0,2,8]},"predicts":"Ibaraki's disruption dominated by typhoon season (August-October) with a secondary early-summer rainy-season bump in June.","shelters":[{"name":"Mito Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Mito"}],"places":[{"name":"Mito City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Mito","nearest":"Mito Community Shelter"}],"towns":["Mito"],"typhoonGrade":null,"typhoonRealData":null},"tochigi":{"name":"Tochigi","archetype":"kanto","capital":"Utsunomiya","hazards":{"typhoon":44,"rain":36,"flood":24,"landslide":14,"thunder":32,"snow":8},"monthly":{"disruption":[20,18,22,24,28,40,36,50,58,42,24,20],"typhoon":[1,1,2,4,8,14,20,42,50,28,6,2],"flood":[10,10,14,18,24,38,34,32,30,22,14,10],"landslide":[4,4,6,8,12,20,22,18,16,10,6,5],"snow":[10,12,4,0,0,0,0,0,0,0,2,8]},"predicts":"Tochigi's disruption dominated by typhoon season (August-October) with a secondary early-summer rainy-season bump in June.","shelters":[{"name":"Utsunomiya Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Utsunomiya"}],"places":[{"name":"Utsunomiya City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Utsunomiya","nearest":"Utsunomiya Community Shelter"}],"towns":["Utsunomiya"],"typhoonGrade":null,"typhoonRealData":null},"gunma":{"name":"Gunma","archetype":"kanto","capital":"Maebashi","hazards":{"typhoon":44,"rain":36,"flood":24,"landslide":14,"thunder":32,"snow":8},"monthly":{"disruption":[20,18,22,24,28,40,36,50,58,42,24,20],"typhoon":[1,1,2,4,8,14,20,42,50,28,6,2],"flood":[10,10,14,18,24,38,34,32,30,22,14,10],"landslide":[4,4,6,8,12,20,22,18,16,10,6,5],"snow":[10,12,4,0,0,0,0,0,0,0,2,8]},"predicts":"Gunma's disruption dominated by typhoon season (August-October) with a secondary early-summer rainy-season bump in June.","shelters":[{"name":"Maebashi Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Maebashi"}],"places":[{"name":"Maebashi City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Maebashi","nearest":"Maebashi Community Shelter"}],"towns":["Maebashi"],"typhoonGrade":null,"typhoonRealData":null},"saitama":{"name":"Saitama","archetype":"kanto","capital":"Saitama","hazards":{"typhoon":44,"rain":36,"flood":24,"landslide":14,"thunder":32,"snow":8},"monthly":{"disruption":[20,18,22,24,28,40,36,50,58,42,24,20],"typhoon":[1,1,2,4,8,14,20,42,50,28,6,2],"flood":[10,10,14,18,24,38,34,32,30,22,14,10],"landslide":[4,4,6,8,12,20,22,18,16,10,6,5],"snow":[10,12,4,0,0,0,0,0,0,0,2,8]},"predicts":"Saitama's disruption dominated by typhoon season (August-October) with a secondary early-summer rainy-season bump in June.","shelters":[{"name":"Saitama Sports Arena","jp":"\\u57fc\\u7389\\u30b9\\u30dd\\u30fc\\u30c4\\u30a2\\u30ea\\u30fc\\u30ca","note":"Large capacity, family area","loc":"Saitama"}],"places":[{"name":"Kawagoe Old Town","jp":"\\u5ddd\\u8d8a","note":"Preserved Edo-period merchant streets","loc":"Kawagoe","nearest":"Saitama Sports Arena"}],"towns":["Kawagoe","Saitama"],"typhoonGrade":null,"typhoonRealData":null},"chiba":{"name":"Chiba","archetype":"kanto","capital":"Chiba","hazards":{"typhoon":16,"rain":36,"flood":24,"landslide":14,"thunder":32,"snow":8},"monthly":{"disruption":[20,18,22,24,28,40,36,50,58,42,24,20],"typhoon":[0,0,1,1,3,4,6,13,16,9,2,1],"flood":[10,10,14,18,24,38,34,32,30,22,14,10],"landslide":[4,4,6,8,12,20,22,18,16,10,6,5],"snow":[10,12,4,0,0,0,0,0,0,0,2,8]},"predicts":"Chiba's disruption dominated by typhoon season (August-October) with a secondary early-summer rainy-season bump in June.","shelters":[{"name":"Chiba Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Chiba"}],"places":[{"name":"Chiba City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Chiba","nearest":"Chiba Community Shelter"}],"towns":["Chiba"],"typhoonGrade":"Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":5,"max_wind_kmh":148.2,"grade_counts":{"3":1,"4":2,"5":2}}},"tokyo":{"name":"Tokyo","archetype":"kanto","capital":"Tokyo","hazards":{"typhoon":44,"rain":36,"flood":24,"landslide":14,"thunder":32,"snow":8},"monthly":{"disruption":[20,18,22,24,28,40,36,50,58,42,24,20],"typhoon":[1,1,2,4,8,14,20,42,50,28,6,2],"flood":[10,10,14,18,24,38,34,32,30,22,14,10],"landslide":[4,4,6,8,12,20,22,18,16,10,6,5],"snow":[10,12,4,0,0,0,0,0,0,0,2,8]},"predicts":"Tokyo's disruption dominated by typhoon season (August-October) with a secondary early-summer rainy-season bump in June.","shelters":[{"name":"Tokyo Metropolitan Gym","jp":"\\u6771\\u4eac\\u90fd\\u7acb\\u4f53\\u80b2\\u9928","note":"English support, near hospital","loc":"Tokyo"}],"places":[{"name":"Senso-ji Temple","jp":"\\u6d45\\u8349\\u5bfa","note":"Tokyo's oldest temple, in the Asakusa district","loc":"Tokyo","nearest":"Tokyo Metropolitan Gym"}],"towns":["Tokyo"],"typhoonGrade":null,"typhoonRealData":null},"kanagawa":{"name":"Kanagawa","archetype":"kanto","capital":"Yokohama","hazards":{"typhoon":41,"rain":36,"flood":24,"landslide":14,"thunder":32,"snow":8},"monthly":{"disruption":[20,18,22,24,28,40,36,50,58,42,24,20],"typhoon":[1,1,2,3,7,11,16,34,41,23,5,2],"flood":[10,10,14,18,24,38,34,32,30,22,14,10],"landslide":[4,4,6,8,12,20,22,18,16,10,6,5],"snow":[10,12,4,0,0,0,0,0,0,0,2,8]},"predicts":"Kanagawa's disruption dominated by typhoon season (August-October) with a secondary early-summer rainy-season bump in June.","shelters":[{"name":"Yokohama Bay Center","jp":"\\u6a2a\\u6d5c\\u30d9\\u30a4\\u30bb\\u30f3\\u30bf\\u30fc","note":"Tourist assistance desk","loc":"Yokohama"}],"places":[{"name":"Minato Mirai","jp":"\\u307f\\u306a\\u3068\\u307f\\u3089\\u3044","note":"Waterfront district with skyline views","loc":"Yokohama","nearest":"Yokohama Bay Center"}],"towns":["Yokohama"],"typhoonGrade":"Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":13,"max_wind_kmh":148.2,"grade_counts":{"3":4,"4":3,"5":6}}},"niigata":{"name":"Niigata","archetype":"chubu","capital":"Niigata","hazards":{"typhoon":32,"rain":30,"flood":22,"landslide":28,"thunder":28,"snow":46},"monthly":{"disruption":[36,32,26,20,22,34,38,36,34,24,26,40],"typhoon":[2,2,3,5,8,12,18,30,28,16,6,3],"flood":[8,8,12,16,22,32,34,30,26,18,12,10],"landslide":[10,10,14,18,26,36,38,32,26,18,12,10],"snow":[58,52,30,8,0,0,0,0,0,2,22,50]},"predicts":"Niigata's mountainous terrain drives elevated landslide risk through the rainy season, alongside notable alpine snowfall December-February.","shelters":[{"name":"Niigata Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Niigata"}],"places":[{"name":"Niigata City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Niigata","nearest":"Niigata Community Shelter"}],"towns":["Niigata"],"typhoonGrade":null,"typhoonRealData":null},"toyama":{"name":"Toyama","archetype":"chubu","capital":"Toyama","hazards":{"typhoon":32,"rain":30,"flood":22,"landslide":28,"thunder":28,"snow":46},"monthly":{"disruption":[36,32,26,20,22,34,38,36,34,24,26,40],"typhoon":[2,2,3,5,8,12,18,30,28,16,6,3],"flood":[8,8,12,16,22,32,34,30,26,18,12,10],"landslide":[10,10,14,18,26,36,38,32,26,18,12,10],"snow":[58,52,30,8,0,0,0,0,0,2,22,50]},"predicts":"Toyama's mountainous terrain drives elevated landslide risk through the rainy season, alongside notable alpine snowfall December-February.","shelters":[{"name":"Toyama Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Toyama"}],"places":[{"name":"Toyama City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Toyama","nearest":"Toyama Community Shelter"}],"towns":["Toyama"],"typhoonGrade":null,"typhoonRealData":null},"ishikawa":{"name":"Ishikawa","archetype":"chubu","capital":"Kanazawa","hazards":{"typhoon":32,"rain":30,"flood":22,"landslide":28,"thunder":28,"snow":46},"monthly":{"disruption":[36,32,26,20,22,34,38,36,34,24,26,40],"typhoon":[2,2,3,5,8,12,18,30,28,16,6,3],"flood":[8,8,12,16,22,32,34,30,26,18,12,10],"landslide":[10,10,14,18,26,36,38,32,26,18,12,10],"snow":[58,52,30,8,0,0,0,0,0,2,22,50]},"predicts":"Ishikawa's mountainous terrain drives elevated landslide risk through the rainy season, alongside notable alpine snowfall December-February.","shelters":[{"name":"Kanazawa Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Kanazawa"}],"places":[{"name":"Kanazawa City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Kanazawa","nearest":"Kanazawa Community Shelter"}],"towns":["Kanazawa"],"typhoonGrade":null,"typhoonRealData":null},"fukui":{"name":"Fukui","archetype":"chubu","capital":"Fukui","hazards":{"typhoon":3,"rain":30,"flood":22,"landslide":28,"thunder":28,"snow":46},"monthly":{"disruption":[36,32,26,20,22,34,38,36,34,24,26,40],"typhoon":[0,0,0,0,1,1,2,3,3,2,1,0],"flood":[8,8,12,16,22,32,34,30,26,18,12,10],"landslide":[10,10,14,18,26,36,38,32,26,18,12,10],"snow":[58,52,30,8,0,0,0,0,0,2,22,50]},"predicts":"Fukui's mountainous terrain drives elevated landslide risk through the rainy season, alongside notable alpine snowfall December-February.","shelters":[{"name":"Fukui Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Fukui"}],"places":[{"name":"Fukui City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Fukui","nearest":"Fukui Community Shelter"}],"towns":["Fukui"],"typhoonGrade":"Typhoon","typhoonRealData":{"landfalls_2000_2025":1,"max_wind_kmh":64.8,"grade_counts":{"3":1,"4":0,"5":0}}},"yamanashi":{"name":"Yamanashi","archetype":"chubu","capital":"Kofu","hazards":{"typhoon":32,"rain":30,"flood":22,"landslide":28,"thunder":28,"snow":46},"monthly":{"disruption":[36,32,26,20,22,34,38,36,34,24,26,40],"typhoon":[2,2,3,5,8,12,18,30,28,16,6,3],"flood":[8,8,12,16,22,32,34,30,26,18,12,10],"landslide":[10,10,14,18,26,36,38,32,26,18,12,10],"snow":[58,52,30,8,0,0,0,0,0,2,22,50]},"predicts":"Yamanashi's mountainous terrain drives elevated landslide risk through the rainy season, alongside notable alpine snowfall December-February.","shelters":[{"name":"Kofu Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Kofu"}],"places":[{"name":"Kofu City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Kofu","nearest":"Kofu Community Shelter"}],"towns":["Kofu"],"typhoonGrade":null,"typhoonRealData":null},"nagano":{"name":"Nagano","archetype":"chubu","capital":"Nagano","hazards":{"typhoon":32,"rain":30,"flood":22,"landslide":28,"thunder":28,"snow":46},"monthly":{"disruption":[36,32,26,20,22,34,38,36,34,24,26,40],"typhoon":[2,2,3,5,8,12,18,30,28,16,6,3],"flood":[8,8,12,16,22,32,34,30,26,18,12,10],"landslide":[10,10,14,18,26,36,38,32,26,18,12,10],"snow":[58,52,30,8,0,0,0,0,0,2,22,50]},"predicts":"Nagano's mountainous terrain drives elevated landslide risk through the rainy season, alongside notable alpine snowfall December-February.","shelters":[{"name":"Nagano Alpine Shelter","jp":"\\u9577\\u91ce\\u30a2\\u30eb\\u30d1\\u30a4\\u30f3\\u30b7\\u30a7\\u30eb\\u30bf\\u30fc","note":"Elevated, snow-rated structure","loc":"Nagano"}],"places":[{"name":"Kamikochi Valley","jp":"\\u4e0a\\u9ad8\\u5730","note":"Alpine valley, popular hiking base","loc":"Nagano","nearest":"Nagano Alpine Shelter"}],"towns":["Nagano"],"typhoonGrade":null,"typhoonRealData":null},"gifu":{"name":"Gifu","archetype":"chubu","capital":"Gifu","hazards":{"typhoon":32,"rain":30,"flood":22,"landslide":28,"thunder":28,"snow":46},"monthly":{"disruption":[36,32,26,20,22,34,38,36,34,24,26,40],"typhoon":[2,2,3,5,8,12,18,30,28,16,6,3],"flood":[8,8,12,16,22,32,34,30,26,18,12,10],"landslide":[10,10,14,18,26,36,38,32,26,18,12,10],"snow":[58,52,30,8,0,0,0,0,0,2,22,50]},"predicts":"Gifu's mountainous terrain drives elevated landslide risk through the rainy season, alongside notable alpine snowfall December-February.","shelters":[],"places":[{"name":"Shirakawa-go","jp":"\\u767d\\u5ddd\\u90f7","note":"UNESCO village of thatched-roof farmhouses","loc":"Gifu","nearest":"\\u2014"}],"towns":["Gifu"],"typhoonGrade":null,"typhoonRealData":null},"shizuoka":{"name":"Shizuoka","archetype":"chubu","capital":"Shizuoka","hazards":{"typhoon":44,"rain":30,"flood":22,"landslide":28,"thunder":28,"snow":46},"monthly":{"disruption":[36,32,26,20,22,34,38,36,34,24,26,40],"typhoon":[3,3,4,7,12,18,26,44,41,23,9,4],"flood":[8,8,12,16,22,32,34,30,26,18,12,10],"landslide":[10,10,14,18,26,36,38,32,26,18,12,10],"snow":[58,52,30,8,0,0,0,0,0,2,22,50]},"predicts":"Shizuoka's mountainous terrain drives elevated landslide risk through the rainy season, alongside notable alpine snowfall December-February.","shelters":[{"name":"Shizuoka Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Shizuoka"}],"places":[{"name":"Shizuoka City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Shizuoka","nearest":"Shizuoka Community Shelter"}],"towns":["Shizuoka"],"typhoonGrade":"Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":14,"max_wind_kmh":148.2,"grade_counts":{"3":5,"4":2,"5":7}}},"aichi":{"name":"Aichi","archetype":"chubu","capital":"Nagoya","hazards":{"typhoon":16,"rain":30,"flood":22,"landslide":28,"thunder":28,"snow":46},"monthly":{"disruption":[36,32,26,20,22,34,38,36,34,24,26,40],"typhoon":[1,1,2,3,4,6,10,16,15,9,3,2],"flood":[8,8,12,16,22,32,34,30,26,18,12,10],"landslide":[10,10,14,18,26,36,38,32,26,18,12,10],"snow":[58,52,30,8,0,0,0,0,0,2,22,50]},"predicts":"Aichi's mountainous terrain drives elevated landslide risk through the rainy season, alongside notable alpine snowfall December-February.","shelters":[{"name":"Nagoya Central Hall","jp":"\\u540d\\u53e4\\u5c4b\\u4e2d\\u592e\\u30db\\u30fc\\u30eb","note":"English support, near station","loc":"Nagoya"}],"places":[{"name":"Nagoya Castle","jp":"\\u540d\\u53e4\\u5c4b\\u57ce","note":"Reconstructed feudal-era castle and grounds","loc":"Nagoya","nearest":"Nagoya Central Hall"}],"towns":["Nagoya"],"typhoonGrade":"Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":5,"max_wind_kmh":129.6,"grade_counts":{"3":2,"4":1,"5":2}}},"mie":{"name":"Mie","archetype":"kansai","capital":"Tsu","hazards":{"typhoon":22,"rain":32,"flood":20,"landslide":18,"thunder":30,"snow":6},"monthly":{"disruption":[18,16,20,22,26,38,34,46,52,38,22,18],"typhoon":[0,0,1,2,3,6,9,18,22,12,3,1],"flood":[8,8,12,16,22,34,30,28,26,18,12,9],"landslide":[5,5,8,10,14,22,24,20,18,12,8,6],"snow":[8,10,3,0,0,0,0,0,0,0,1,6]},"predicts":"Mie's typhoon-led risk peaking August-September, with a mild rainy-season rise in June and low snow risk overall.","shelters":[{"name":"Tsu Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Tsu"}],"places":[{"name":"Tsu City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Tsu","nearest":"Tsu Community Shelter"}],"towns":["Tsu"],"typhoonGrade":"Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":7,"max_wind_kmh":138.9,"grade_counts":{"3":2,"4":1,"5":4}}},"shiga":{"name":"Shiga","archetype":"kansai","capital":"Otsu","hazards":{"typhoon":40,"rain":32,"flood":20,"landslide":18,"thunder":30,"snow":6},"monthly":{"disruption":[18,16,20,22,26,38,34,46,52,38,22,18],"typhoon":[1,1,2,4,7,12,18,38,46,26,6,2],"flood":[8,8,12,16,22,34,30,28,26,18,12,9],"landslide":[5,5,8,10,14,22,24,20,18,12,8,6],"snow":[8,10,3,0,0,0,0,0,0,0,1,6]},"predicts":"Shiga's typhoon-led risk peaking August-September, with a mild rainy-season rise in June and low snow risk overall.","shelters":[{"name":"Otsu Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Otsu"}],"places":[{"name":"Otsu City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Otsu","nearest":"Otsu Community Shelter"}],"towns":["Otsu"],"typhoonGrade":null,"typhoonRealData":null},"kyoto":{"name":"Kyoto","archetype":"kansai","capital":"Kyoto","hazards":{"typhoon":40,"rain":32,"flood":20,"landslide":18,"thunder":30,"snow":6},"monthly":{"disruption":[18,16,20,22,26,38,34,46,52,38,22,18],"typhoon":[1,1,2,4,7,12,18,38,46,26,6,2],"flood":[8,8,12,16,22,34,30,28,26,18,12,9],"landslide":[5,5,8,10,14,22,24,20,18,12,8,6],"snow":[8,10,3,0,0,0,0,0,0,0,1,6]},"predicts":"Kyoto's typhoon-led risk peaking August-September, with a mild rainy-season rise in June and low snow risk overall.","shelters":[{"name":"Kyoto Heritage Shelter","jp":"\\u4eac\\u90fd\\u6587\\u5316\\u907f\\u96e3\\u6240","note":"Tourist assistance desk","loc":"Kyoto"}],"places":[{"name":"Fushimi Inari Shrine","jp":"\\u4f0f\\u898b\\u7a32\\u8377\\u5927\\u793e","note":"Thousands of vermilion torii gates","loc":"Kyoto","nearest":"Kyoto Heritage Shelter"}],"towns":["Kyoto"],"typhoonGrade":null,"typhoonRealData":null},"osaka":{"name":"Osaka","archetype":"kansai","capital":"Osaka","hazards":{"typhoon":3,"rain":32,"flood":20,"landslide":18,"thunder":30,"snow":6},"monthly":{"disruption":[18,16,20,22,26,38,34,46,52,38,22,18],"typhoon":[0,0,0,0,0,1,1,2,3,2,0,0],"flood":[8,8,12,16,22,34,30,28,26,18,12,9],"landslide":[5,5,8,10,14,22,24,20,18,12,8,6],"snow":[8,10,3,0,0,0,0,0,0,0,1,6]},"predicts":"Osaka's typhoon-led risk peaking August-September, with a mild rainy-season rise in June and low snow risk overall.","shelters":[{"name":"Osaka Riverfront Hall","jp":"\\u5927\\u962a\\u30ea\\u30d0\\u30fc\\u30d5\\u30ed\\u30f3\\u30c8\\u30db\\u30fc\\u30eb","note":"English support, flood-safe elevation","loc":"Osaka"}],"places":[{"name":"Dotonbori","jp":"\\u9053\\u9813\\u5800","note":"Osaka's iconic canal-side dining district","loc":"Osaka","nearest":"Osaka Riverfront Hall"}],"towns":["Osaka"],"typhoonGrade":"Typhoon","typhoonRealData":{"landfalls_2000_2025":1,"max_wind_kmh":92.6,"grade_counts":{"3":0,"4":1,"5":0}}},"hyogo":{"name":"Hyogo","archetype":"kansai","capital":"Kobe","hazards":{"typhoon":9,"rain":32,"flood":20,"landslide":18,"thunder":30,"snow":6},"monthly":{"disruption":[18,16,20,22,26,38,34,46,52,38,22,18],"typhoon":[0,0,0,1,1,2,4,7,9,5,1,0],"flood":[8,8,12,16,22,34,30,28,26,18,12,9],"landslide":[5,5,8,10,14,22,24,20,18,12,8,6],"snow":[8,10,3,0,0,0,0,0,0,0,1,6]},"predicts":"Hyogo's typhoon-led risk peaking August-September, with a mild rainy-season rise in June and low snow risk overall.","shelters":[{"name":"Kobe Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Kobe"}],"places":[{"name":"Kobe City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Kobe","nearest":"Kobe Community Shelter"}],"towns":["Kobe"],"typhoonGrade":"Typhoon","typhoonRealData":{"landfalls_2000_2025":3,"max_wind_kmh":111.1,"grade_counts":{"3":0,"4":3,"5":0}}},"nara":{"name":"Nara","archetype":"kansai","capital":"Nara","hazards":{"typhoon":40,"rain":32,"flood":20,"landslide":18,"thunder":30,"snow":6},"monthly":{"disruption":[18,16,20,22,26,38,34,46,52,38,22,18],"typhoon":[1,1,2,4,7,12,18,38,46,26,6,2],"flood":[8,8,12,16,22,34,30,28,26,18,12,9],"landslide":[5,5,8,10,14,22,24,20,18,12,8,6],"snow":[8,10,3,0,0,0,0,0,0,0,1,6]},"predicts":"Nara's typhoon-led risk peaking August-September, with a mild rainy-season rise in June and low snow risk overall.","shelters":[],"places":[{"name":"Nara Park","jp":"\\u5948\\u826f\\u516c\\u5712","note":"Free-roaming deer and Todai-ji temple","loc":"Nara","nearest":"\\u2014"}],"towns":["Nara"],"typhoonGrade":null,"typhoonRealData":null},"wakayama":{"name":"Wakayama","archetype":"kansai","capital":"Wakayama","hazards":{"typhoon":38,"rain":32,"flood":20,"landslide":18,"thunder":30,"snow":6},"monthly":{"disruption":[18,16,20,22,26,38,34,46,52,38,22,18],"typhoon":[1,1,2,3,6,10,15,31,38,21,5,2],"flood":[8,8,12,16,22,34,30,28,26,18,12,9],"landslide":[5,5,8,10,14,22,24,20,18,12,8,6],"snow":[8,10,3,0,0,0,0,0,0,0,1,6]},"predicts":"Wakayama's typhoon-led risk peaking August-September, with a mild rainy-season rise in June and low snow risk overall.","shelters":[{"name":"Wakayama Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Wakayama"}],"places":[{"name":"Wakayama City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Wakayama","nearest":"Wakayama Community Shelter"}],"towns":["Wakayama"],"typhoonGrade":"Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":12,"max_wind_kmh":148.2,"grade_counts":{"3":1,"4":8,"5":3}}},"tottori":{"name":"Tottori","archetype":"chugoku","capital":"Tottori","hazards":{"typhoon":34,"rain":40,"flood":30,"landslide":26,"thunder":26,"snow":12},"monthly":{"disruption":[24,20,22,24,30,48,46,40,36,26,22,22],"typhoon":[1,1,2,4,7,12,18,32,30,16,5,2],"flood":[10,10,14,18,26,44,42,32,28,18,12,10],"landslide":[8,8,12,16,24,38,36,26,22,14,10,8],"snow":[14,14,5,0,0,0,0,0,0,0,3,12]},"predicts":"Tottori's heightened flood and landslide risk during the June-July rainy season, consistent with historical flood events in the region.","shelters":[{"name":"Tottori Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Tottori"}],"places":[{"name":"Tottori City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Tottori","nearest":"Tottori Community Shelter"}],"towns":["Tottori"],"typhoonGrade":null,"typhoonRealData":null},"shimane":{"name":"Shimane","archetype":"chugoku","capital":"Matsue","hazards":{"typhoon":34,"rain":40,"flood":30,"landslide":26,"thunder":26,"snow":12},"monthly":{"disruption":[24,20,22,24,30,48,46,40,36,26,22,22],"typhoon":[1,1,2,4,7,12,18,32,30,16,5,2],"flood":[10,10,14,18,26,44,42,32,28,18,12,10],"landslide":[8,8,12,16,24,38,36,26,22,14,10,8],"snow":[14,14,5,0,0,0,0,0,0,0,3,12]},"predicts":"Shimane's heightened flood and landslide risk during the June-July rainy season, consistent with historical flood events in the region.","shelters":[{"name":"Matsue Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Matsue"}],"places":[{"name":"Matsue City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Matsue","nearest":"Matsue Community Shelter"}],"towns":["Matsue"],"typhoonGrade":null,"typhoonRealData":null},"okayama":{"name":"Okayama","archetype":"chugoku","capital":"Okayama","hazards":{"typhoon":6,"rain":40,"flood":30,"landslide":26,"thunder":26,"snow":12},"monthly":{"disruption":[24,20,22,24,30,48,46,40,36,26,22,22],"typhoon":[0,0,0,1,1,2,3,6,6,3,1,0],"flood":[10,10,14,18,26,44,42,32,28,18,12,10],"landslide":[8,8,12,16,24,38,36,26,22,14,10,8],"snow":[14,14,5,0,0,0,0,0,0,0,3,12]},"predicts":"Okayama's heightened flood and landslide risk during the June-July rainy season, consistent with historical flood events in the region.","shelters":[{"name":"Okayama River Center","jp":"\\u5ca1\\u5c71\\u30ea\\u30d0\\u30fc\\u30bb\\u30f3\\u30bf\\u30fc","note":"Elevated ground, flood-safe","loc":"Okayama"}],"places":[{"name":"Kurashiki Bikan","jp":"\\u5009\\u6577\\u7f8e\\u89b3\\u5730\\u533a","note":"Canal town with preserved merchant houses","loc":"Okayama","nearest":"Okayama River Center"}],"towns":["Okayama"],"typhoonGrade":"Typhoon","typhoonRealData":{"landfalls_2000_2025":2,"max_wind_kmh":101.9,"grade_counts":{"3":1,"4":1,"5":0}}},"hiroshima":{"name":"Hiroshima","archetype":"chugoku","capital":"Hiroshima","hazards":{"typhoon":9,"rain":40,"flood":30,"landslide":26,"thunder":26,"snow":12},"monthly":{"disruption":[24,20,22,24,30,48,46,40,36,26,22,22],"typhoon":[0,0,1,1,2,3,5,9,8,4,1,1],"flood":[10,10,14,18,26,44,42,32,28,18,12,10],"landslide":[8,8,12,16,24,38,36,26,22,14,10,8],"snow":[14,14,5,0,0,0,0,0,0,0,3,12]},"predicts":"Hiroshima's heightened flood and landslide risk during the June-July rainy season, consistent with historical flood events in the region.","shelters":[{"name":"Hiroshima Peace Hall","jp":"\\u5e83\\u5cf6\\u5e73\\u548c\\u30db\\u30fc\\u30eb","note":"English support, large capacity","loc":"Hiroshima"}],"places":[{"name":"Itsukushima Shrine","jp":"\\u53b3\\u5cf6\\u795e\\u793e","note":"Floating torii gate on Miyajima island","loc":"Hiroshima","nearest":"Hiroshima Peace Hall"}],"towns":["Hiroshima"],"typhoonGrade":"Typhoon","typhoonRealData":{"landfalls_2000_2025":3,"max_wind_kmh":83.3,"grade_counts":{"3":3,"4":0,"5":0}}},"yamaguchi":{"name":"Yamaguchi","archetype":"chugoku","capital":"Yamaguchi","hazards":{"typhoon":9,"rain":40,"flood":30,"landslide":26,"thunder":26,"snow":12},"monthly":{"disruption":[24,20,22,24,30,48,46,40,36,26,22,22],"typhoon":[0,0,1,1,2,3,5,9,8,4,1,1],"flood":[10,10,14,18,26,44,42,32,28,18,12,10],"landslide":[8,8,12,16,24,38,36,26,22,14,10,8],"snow":[14,14,5,0,0,0,0,0,0,0,3,12]},"predicts":"Yamaguchi's heightened flood and landslide risk during the June-July rainy season, consistent with historical flood events in the region.","shelters":[{"name":"Yamaguchi Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Yamaguchi"}],"places":[{"name":"Yamaguchi City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Yamaguchi","nearest":"Yamaguchi Community Shelter"}],"towns":["Yamaguchi"],"typhoonGrade":"Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":3,"max_wind_kmh":129.6,"grade_counts":{"3":1,"4":1,"5":1}}},"tokushima":{"name":"Tokushima","archetype":"shikoku","capital":"Tokushima","hazards":{"typhoon":38,"rain":36,"flood":24,"landslide":24,"thunder":26,"snow":4},"monthly":{"disruption":[18,16,20,22,28,42,40,54,56,36,20,18],"typhoon":[1,1,2,4,7,11,17,35,38,19,5,2],"flood":[9,9,13,17,24,38,34,30,28,18,12,10],"landslide":[7,7,11,15,22,32,32,26,22,14,10,8],"snow":[6,7,2,0,0,0,0,0,0,0,1,5]},"predicts":"Tokushima's exposed to the Pacific, sees the country's sharpest typhoon-season spike in August-September, alongside a rainy-season flood rise in June.","shelters":[{"name":"Tokushima Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Tokushima"}],"places":[{"name":"Tokushima City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Tokushima","nearest":"Tokushima Community Shelter"}],"towns":["Tokushima"],"typhoonGrade":"Very Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":12,"max_wind_kmh":157.4,"grade_counts":{"3":2,"4":4,"5":6}}},"kagawa":{"name":"Kagawa","archetype":"shikoku","capital":"Takamatsu","hazards":{"typhoon":3,"rain":36,"flood":24,"landslide":24,"thunder":26,"snow":4},"monthly":{"disruption":[18,16,20,22,28,42,40,54,56,36,20,18],"typhoon":[0,0,0,0,1,1,1,3,3,2,0,0],"flood":[9,9,13,17,24,38,34,30,28,18,12,10],"landslide":[7,7,11,15,22,32,32,26,22,14,10,8],"snow":[6,7,2,0,0,0,0,0,0,0,1,5]},"predicts":"Kagawa's exposed to the Pacific, sees the country's sharpest typhoon-season spike in August-September, alongside a rainy-season flood rise in June.","shelters":[{"name":"Takamatsu Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Takamatsu"}],"places":[{"name":"Takamatsu City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Takamatsu","nearest":"Takamatsu Community Shelter"}],"towns":["Takamatsu"],"typhoonGrade":"Typhoon","typhoonRealData":{"landfalls_2000_2025":1,"max_wind_kmh":83.3,"grade_counts":{"3":1,"4":0,"5":0}}},"ehime":{"name":"Ehime","archetype":"shikoku","capital":"Matsuyama","hazards":{"typhoon":9,"rain":36,"flood":24,"landslide":24,"thunder":26,"snow":4},"monthly":{"disruption":[18,16,20,22,28,42,40,54,56,36,20,18],"typhoon":[0,0,0,1,2,3,4,8,9,4,1,0],"flood":[9,9,13,17,24,38,34,30,28,18,12,10],"landslide":[7,7,11,15,22,32,32,26,22,14,10,8],"snow":[6,7,2,0,0,0,0,0,0,0,1,5]},"predicts":"Ehime's exposed to the Pacific, sees the country's sharpest typhoon-season spike in August-September, alongside a rainy-season flood rise in June.","shelters":[{"name":"Matsuyama Coastal Hall","jp":"\\u677e\\u5c71\\u6cbf\\u5cb8\\u30db\\u30fc\\u30eb","note":"English support, storm-rated","loc":"Matsuyama"}],"places":[{"name":"Dogo Onsen","jp":"\\u9053\\u5f8c\\u6e29\\u6cc9","note":"One of Japan's oldest hot spring bathhouses","loc":"Matsuyama","nearest":"Matsuyama Coastal Hall"}],"towns":["Matsuyama"],"typhoonGrade":"Typhoon","typhoonRealData":{"landfalls_2000_2025":3,"max_wind_kmh":101.9,"grade_counts":{"3":1,"4":2,"5":0}}},"kochi":{"name":"Kochi","archetype":"shikoku","capital":"Kochi","hazards":{"typhoon":44,"rain":36,"flood":24,"landslide":24,"thunder":26,"snow":4},"monthly":{"disruption":[18,16,20,22,28,42,40,54,56,36,20,18],"typhoon":[1,1,2,5,8,13,20,40,44,22,6,2],"flood":[9,9,13,17,24,38,34,30,28,18,12,10],"landslide":[7,7,11,15,22,32,32,26,22,14,10,8],"snow":[6,7,2,0,0,0,0,0,0,0,1,5]},"predicts":"Kochi's exposed to the Pacific, sees the country's sharpest typhoon-season spike in August-September, alongside a rainy-season flood rise in June.","shelters":[{"name":"Kochi Emergency Center","jp":"\\u9ad8\\u77e5\\u7dca\\u6025\\u30bb\\u30f3\\u30bf\\u30fc","note":"Tourist assistance desk","loc":"Kochi"}],"places":[{"name":"Katsurahama Beach","jp":"\\u6842\\u6d5c","note":"Scenic coastline with a famous statue","loc":"Kochi","nearest":"Kochi Emergency Center"}],"towns":["Kochi"],"typhoonGrade":"Very Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":14,"max_wind_kmh":157.4,"grade_counts":{"3":2,"4":2,"5":10}}},"fukuoka":{"name":"Fukuoka","archetype":"kyushu","capital":"Fukuoka","hazards":{"typhoon":12,"rain":44,"flood":32,"landslide":28,"thunder":28,"snow":3},"monthly":{"disruption":[20,18,22,26,34,52,50,48,44,30,22,20],"typhoon":[1,1,1,2,3,4,7,11,12,6,2,1],"flood":[12,12,16,22,30,48,46,34,30,20,14,12],"landslide":[9,9,13,18,26,40,38,28,24,16,11,9],"snow":[4,5,2,0,0,0,0,0,0,0,1,3]},"predicts":"Fukuoka's faces the country's earliest and heaviest typhoon exposure, plus severe rainy-season flooding in June-July.","shelters":[{"name":"Fukuoka Central Shelter","jp":"\\u798f\\u5ca1\\u4e2d\\u592e\\u907f\\u96e3\\u6240","note":"English support, near hospital","loc":"Fukuoka"}],"places":[{"name":"Dazaifu Tenmangu","jp":"\\u592a\\u5bb0\\u5e9c\\u5929\\u6e80\\u5bae","note":"Historic shrine dedicated to Sugawara Michizane","loc":"Fukuoka","nearest":"Fukuoka Central Shelter"}],"towns":["Fukuoka"],"typhoonGrade":"Typhoon","typhoonRealData":{"landfalls_2000_2025":4,"max_wind_kmh":111.1,"grade_counts":{"3":1,"4":3,"5":0}}},"saga":{"name":"Saga","archetype":"kyushu","capital":"Saga","hazards":{"typhoon":3,"rain":44,"flood":32,"landslide":28,"thunder":28,"snow":3},"monthly":{"disruption":[20,18,22,26,34,52,50,48,44,30,22,20],"typhoon":[0,0,0,0,1,1,2,3,3,2,0,0],"flood":[12,12,16,22,30,48,46,34,30,20,14,12],"landslide":[9,9,13,18,26,40,38,28,24,16,11,9],"snow":[4,5,2,0,0,0,0,0,0,0,1,3]},"predicts":"Saga's faces the country's earliest and heaviest typhoon exposure, plus severe rainy-season flooding in June-July.","shelters":[{"name":"Saga Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Saga"}],"places":[{"name":"Saga City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Saga","nearest":"Saga Community Shelter"}],"towns":["Saga"],"typhoonGrade":"Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":1,"max_wind_kmh":129.6,"grade_counts":{"3":0,"4":0,"5":1}}},"nagasaki":{"name":"Nagasaki","archetype":"kyushu","capital":"Nagasaki","hazards":{"typhoon":34,"rain":44,"flood":32,"landslide":28,"thunder":28,"snow":3},"monthly":{"disruption":[20,18,22,26,34,52,50,48,44,30,22,20],"typhoon":[2,2,2,5,8,12,20,32,34,17,5,2],"flood":[12,12,16,22,30,48,46,34,30,20,14,12],"landslide":[9,9,13,18,26,40,38,28,24,16,11,9],"snow":[4,5,2,0,0,0,0,0,0,0,1,3]},"predicts":"Nagasaki's faces the country's earliest and heaviest typhoon exposure, plus severe rainy-season flooding in June-July.","shelters":[{"name":"Nagasaki Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Nagasaki"}],"places":[{"name":"Nagasaki City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Nagasaki","nearest":"Nagasaki Community Shelter"}],"towns":["Nagasaki"],"typhoonGrade":"Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":11,"max_wind_kmh":148.2,"grade_counts":{"3":5,"4":2,"5":4}}},"kumamoto":{"name":"Kumamoto","archetype":"kyushu","capital":"Kumamoto","hazards":{"typhoon":6,"rain":44,"flood":32,"landslide":28,"thunder":28,"snow":3},"monthly":{"disruption":[20,18,22,26,34,52,50,48,44,30,22,20],"typhoon":[0,0,0,1,1,2,4,6,6,3,1,0],"flood":[12,12,16,22,30,48,46,34,30,20,14,12],"landslide":[9,9,13,18,26,40,38,28,24,16,11,9],"snow":[4,5,2,0,0,0,0,0,0,0,1,3]},"predicts":"Kumamoto's faces the country's earliest and heaviest typhoon exposure, plus severe rainy-season flooding in June-July.","shelters":[{"name":"Kumamoto Highland Hall","jp":"\\u718a\\u672c\\u9ad8\\u5730\\u30db\\u30fc\\u30eb","note":"Elevated, flood-safe","loc":"Kumamoto"}],"places":[{"name":"Kumamoto Castle","jp":"\\u718a\\u672c\\u57ce","note":"One of Japan's most celebrated castles","loc":"Kumamoto","nearest":"Kumamoto Highland Hall"}],"towns":["Kumamoto"],"typhoonGrade":"Very Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":2,"max_wind_kmh":157.4,"grade_counts":{"3":0,"4":0,"5":2}}},"oita":{"name":"Oita","archetype":"kyushu","capital":"Oita","hazards":{"typhoon":16,"rain":44,"flood":32,"landslide":28,"thunder":28,"snow":3},"monthly":{"disruption":[20,18,22,26,34,52,50,48,44,30,22,20],"typhoon":[1,1,1,2,4,6,9,15,16,8,3,1],"flood":[12,12,16,22,30,48,46,34,30,20,14,12],"landslide":[9,9,13,18,26,40,38,28,24,16,11,9],"snow":[4,5,2,0,0,0,0,0,0,0,1,3]},"predicts":"Oita's faces the country's earliest and heaviest typhoon exposure, plus severe rainy-season flooding in June-July.","shelters":[{"name":"Oita Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Oita"}],"places":[{"name":"Oita City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Oita","nearest":"Oita Community Shelter"}],"towns":["Oita"],"typhoonGrade":"Typhoon","typhoonRealData":{"landfalls_2000_2025":5,"max_wind_kmh":111.1,"grade_counts":{"3":2,"4":3,"5":0}}},"miyazaki":{"name":"Miyazaki","archetype":"kyushu","capital":"Miyazaki","hazards":{"typhoon":12,"rain":44,"flood":32,"landslide":28,"thunder":28,"snow":3},"monthly":{"disruption":[20,18,22,26,34,52,50,48,44,30,22,20],"typhoon":[1,1,1,2,3,4,7,11,12,6,2,1],"flood":[12,12,16,22,30,48,46,34,30,20,14,12],"landslide":[9,9,13,18,26,40,38,28,24,16,11,9],"snow":[4,5,2,0,0,0,0,0,0,0,1,3]},"predicts":"Miyazaki's faces the country's earliest and heaviest typhoon exposure, plus severe rainy-season flooding in June-July.","shelters":[{"name":"Miyazaki Community Shelter","jp":"\\u907f\\u96e3\\u6240","note":"Designated municipal shelter","loc":"Miyazaki"}],"places":[{"name":"Miyazaki City Center","jp":"\\u5e02\\u8857\\u5730","note":"Central district \\u2014 local sights and services","loc":"Miyazaki","nearest":"Miyazaki Community Shelter"}],"towns":["Miyazaki"],"typhoonGrade":"Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":4,"max_wind_kmh":148.2,"grade_counts":{"3":2,"4":0,"5":2}}},"kagoshima":{"name":"Kagoshima","archetype":"kyushu","capital":"Kagoshima","hazards":{"typhoon":62,"rain":44,"flood":32,"landslide":28,"thunder":28,"snow":3},"monthly":{"disruption":[20,18,22,26,34,52,50,48,44,30,22,20],"typhoon":[3,3,4,8,14,23,37,59,62,31,10,4],"flood":[12,12,16,22,30,48,46,34,30,20,14,12],"landslide":[9,9,13,18,26,40,38,28,24,16,11,9],"snow":[4,5,2,0,0,0,0,0,0,0,1,3]},"predicts":"Kagoshima's faces the country's earliest and heaviest typhoon exposure, plus severe rainy-season flooding in June-July.","shelters":[{"name":"Kagoshima Bay Center","jp":"\\u9e7f\\u5150\\u5cf6\\u6e7e\\u30bb\\u30f3\\u30bf\\u30fc","note":"Volcanic-ash rated roofing","loc":"Kagoshima"}],"places":[{"name":"Sakurajima","jp":"\\u685c\\u5cf6","note":"Active volcano with ferry views across the bay","loc":"Kagoshima","nearest":"Kagoshima Bay Center"}],"towns":["Kagoshima"],"typhoonGrade":"Very Strong Typhoon","typhoonRealData":{"landfalls_2000_2025":20,"max_wind_kmh":166.7,"grade_counts":{"3":2,"4":8,"5":10}}},"okinawa":{"name":"Okinawa","archetype":"okinawa","capital":"Naha","hazards":{"typhoon":100,"rain":24,"flood":14,"landslide":10,"thunder":20,"snow":0},"monthly":{"disruption":[16,14,16,18,24,34,44,50,42,28,18,16],"typhoon":[6,6,8,15,27,42,73,100,85,46,15,8],"flood":[6,6,8,10,14,20,18,16,15,10,7,6],"landslide":[3,3,4,5,7,10,9,8,7,5,4,3],"snow":[0,0,0,0,0,0,0,0,0,0,0,0]},"predicts":"Okinawa's risk is almost entirely typhoon-driven, with the highest activity July-September and negligible snow or landslide risk year-round.","shelters":[{"name":"Naha Storm Shelter","jp":"\\u90a3\\u8987\\u66b4\\u98a8\\u907f\\u96e3\\u6240","note":"English support, storm-rated structure","loc":"Naha"},{"name":"Ishigaki Community Hall","jp":"\\u77f3\\u57a3\\u30b3\\u30df\\u30e5\\u30cb\\u30c6\\u30a3\\u30db\\u30fc\\u30eb","note":"Tourist assistance desk","loc":"Ishigaki"}],"places":[{"name":"Shuri Castle","jp":"\\u9996\\u91cc\\u57ce","note":"Historic Ryukyu Kingdom royal palace grounds","loc":"Naha","nearest":"Naha Storm Shelter"},{"name":"Kabira Bay","jp":"\\u5ddd\\u5e73\\u6e7e","note":"Turquoise waters, glass-bottom boat tours","loc":"Ishigaki","nearest":"Ishigaki Community Hall"}],"towns":["Ishigaki","Naha"],"typhoonGrade":"Violent Typhoon","typhoonRealData":{"landfalls_2000_2025":32,"max_wind_kmh":203.7,"grade_counts":{"3":2,"4":8,"5":22}}}};

const ARCH_LABELS = {
  hokkaido:'Hokkaido', tohoku:'Tohoku', kanto:'Kanto', chubu:'Chubu', kansai:'Kansai',
  chugoku:'Chugoku', shikoku:'Shikoku', kyushu:'Kyushu', okinawa:'Okinawa'
};
const CLIMATE = {
  hokkaido:{temp:'4\\u00b0C',wind:'14 km/h'}, tohoku:{temp:'8\\u00b0C',wind:'12 km/h'},
  kanto:{temp:'16\\u00b0C',wind:'10 km/h'}, chubu:{temp:'11\\u00b0C',wind:'11 km/h'},
  kansai:{temp:'15\\u00b0C',wind:'9 km/h'}, chugoku:{temp:'14\\u00b0C',wind:'12 km/h'},
  shikoku:{temp:'15\\u00b0C',wind:'13 km/h'}, kyushu:{temp:'17\\u00b0C',wind:'15 km/h'},
  okinawa:{temp:'23\\u00b0C',wind:'18 km/h'}
};

const HAZARD_META = [
  {key:'typhoon', label:'Typhoon', icon:'\\ud83c\\udf00'},
  {key:'flood', label:'Flood potential', icon:'\\ud83c\\udfe2'},
  {key:'snow', label:'Heavy snow', icon:'\\u2744\\ufe0f'}
];

// Labels used by the map's disaster-type selector and matching legend.
const MAP_HAZARD_META = [
  {key:'typhoon', label:'Typhoon'},
  {key:'rain', label:'Heavy rain'},
  {key:'flood', label:'Flood'},
  {key:'landslide', label:'Landslide'},
  {key:'thunder', label:'Thunderstorm'},
  {key:'snow', label:'Heavy snow'}
];

function levelFor(pct){
  if(pct < 25) return {cls:'lvl-low', label:'Low', color:'#22C55E'};
  if(pct < 45) return {cls:'lvl-medium', label:'Medium', color:'#F59E0B'};
  return {cls:'lvl-high', label:'High', color:'#EF4444'};
}

function hashStr(str){
  let h = 0;
  for(let i=0;i<str.length;i++){ h = (h*31 + str.charCodeAt(i)) >>> 0; }
  return h;
}

let currentPref = 'tokyo';
let chartPref = 'tokyo';
let selectedMapHazard = 'typhoon';
const SNOW_MODEL_PREFECTURES = new Set(['niigata','yamagata']);
let charts = {};
// Period applied by the last successful Check risk: {from, to, months}. Null = full year.
let activePeriod = null;

/* ---------------- Persistent light/dark theme ---------------- */
const themeToggle = document.getElementById('theme-toggle');
function applyTheme(theme){
  const chosen = theme === 'dark' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', chosen);
  const isDark = chosen === 'dark';
  if(themeToggle){
    themeToggle.setAttribute('aria-pressed', String(isDark));
    themeToggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    const icon = themeToggle.querySelector('.theme-icon');
    const label = themeToggle.querySelector('.theme-label');
    if(icon) icon.textContent = isDark ? '☀' : '☾';
    if(label) label.textContent = isDark ? 'Light mode' : 'Dark mode';
  }
  if(document.getElementById('view-dataviz')?.classList.contains('active')) requestAnimationFrame(renderCharts);
}
let savedTheme = 'light';
try { savedTheme = localStorage.getItem('kikan-theme') || 'light'; } catch(e) {}
applyTheme(savedTheme);
if(themeToggle){
  themeToggle.addEventListener('click', ()=>{
    const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    try { localStorage.setItem('kikan-theme', next); } catch(e) {}
  });
}


/* ---------------- Navigation menu ---------------- */
const menuTrigger = document.getElementById('menu-trigger');
const siteMenu = document.getElementById('site-menu');
function setMenuOpen(open){
  if(!menuTrigger || !siteMenu) return;
  siteMenu.hidden = !open;
  siteMenu.classList.toggle('menu-opening', open);
  menuTrigger.setAttribute('aria-expanded', String(open));
  menuTrigger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  const icon = menuTrigger.querySelector('[aria-hidden="true"]');
  if(icon) icon.textContent = open ? '✕' : '☰';
}
menuTrigger?.addEventListener('click', ()=>setMenuOpen(siteMenu.hidden));
document.addEventListener('click', event=>{
  if(siteMenu && !siteMenu.hidden && !siteMenu.contains(event.target) && !menuTrigger.contains(event.target)) setMenuOpen(false);
});
document.addEventListener('keydown', event=>{
  if(event.key === 'Escape' && siteMenu && !siteMenu.hidden){ setMenuOpen(false); menuTrigger?.focus(); }
});
document.querySelectorAll('nav.tabs button').forEach(btn=>{
  btn.addEventListener('click', ()=> { switchView(btn.dataset.view); setMenuOpen(false); });
});
document.querySelectorAll('[data-goto]').forEach(btn=>{
  btn.addEventListener('click', ()=> switchView(btn.dataset.goto));
});
function switchView(view){
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.getElementById('view-'+view).classList.add('active');
  document.querySelectorAll('nav.tabs button').forEach(b=>{
    const on = b.dataset.view === view;
    b.classList.toggle('active', on);
    b.setAttribute('aria-selected', on);
  });
  if(view === 'dataviz') requestAnimationFrame(renderCharts);
  if(view === 'prediction') requestAnimationFrame(renderPrefLabels);
}

/* ---------------- Map: prefecture click -> select and zoom ---------------- */
document.querySelectorAll('.pref').forEach(el=>{
  el.addEventListener('click', ()=> selectPref(el.dataset.id));
  el.addEventListener('keydown', e=>{ if(e.key==='Enter' || e.key===' '){ e.preventDefault(); selectPref(el.dataset.id); } });
});

/* ---------------- Map: always-on prefecture name labels ---------------- */
function renderPrefLabels(){
  const labelsG = document.getElementById('pref-labels');
  labelsG.innerHTML = '';
  document.querySelectorAll('.pref').forEach(el=>{
    const bbox = el.getBBox();
    const cx = bbox.x + bbox.width/2;
    const cy = bbox.y + bbox.height/2;
    const text = document.createElementNS('http://www.w3.org/2000/svg','text');
    text.setAttribute('class','pref-label');
    text.setAttribute('x', cx);
    text.setAttribute('y', cy);
    text.setAttribute('data-for', el.dataset.id);
    text.textContent = el.getAttribute('aria-label');
    if(el.dataset.id === currentPref){
      text.classList.add('active');
      text.style.opacity = '1';
    } else {
      text.style.opacity = '.18';
    }
    labelsG.appendChild(text);
  });
}

/* ---------------- Map: zoom in/out controls ---------------- */
const VB_CX = 219, VB_CY = 258; // viewBox 0 0 438 516 center
let mapZoom = 0.88;
let panX = 0, panY = 0;
const ZOOM_MIN = 0.88, ZOOM_MAX = 4, ZOOM_STEP = 0.6;

function applyMapZoom(){
  const g = document.getElementById('zoom-g');
  const tx = (1 - mapZoom) * VB_CX + panX;
  const ty = (1 - mapZoom) * VB_CY + panY;
  g.setAttribute('transform', \`translate(\${tx}, \${ty}) scale(\${mapZoom})\`);
  document.getElementById('zoom-out-btn').disabled = mapZoom <= ZOOM_MIN;
  document.getElementById('zoom-in-btn').disabled = mapZoom >= ZOOM_MAX;
  svgEl.style.cursor = mapZoom > ZOOM_MIN ? 'grab' : 'default';
}
document.getElementById('zoom-in-btn').addEventListener('click', ()=>{
  mapZoom = Math.min(ZOOM_MAX, +(mapZoom + ZOOM_STEP).toFixed(2));
  applyMapZoom();
});
document.getElementById('zoom-out-btn').addEventListener('click', ()=>{
  mapZoom = Math.max(ZOOM_MIN, +(mapZoom - ZOOM_STEP).toFixed(2));
  if(mapZoom === ZOOM_MIN){ panX = 0; panY = 0; }
  applyMapZoom();
});
document.getElementById('zoom-reset-btn').addEventListener('click', ()=>{
  mapZoom = ZOOM_MIN; panX = 0; panY = 0;
  applyMapZoom();
});

/* drag to pan, only active once zoomed in — only engages after real movement, so a plain click still reaches the prefecture underneath */
const svgEl = document.getElementById('japan-svg');
let panPointerId = null, isDragging = false;
let dragStartX = 0, dragStartY = 0, panStartX = 0, panStartY = 0;
const DRAG_THRESHOLD = 4;

svgEl.addEventListener('pointerdown', e=>{
  if(mapZoom <= ZOOM_MIN) return;
  panPointerId = e.pointerId;
  dragStartX = e.clientX; dragStartY = e.clientY;
  panStartX = panX; panStartY = panY;
  isDragging = false;
});
svgEl.addEventListener('pointermove', e=>{
  if(panPointerId === null || e.pointerId !== panPointerId) return;
  const dx = e.clientX - dragStartX, dy = e.clientY - dragStartY;
  if(!isDragging && Math.hypot(dx, dy) > DRAG_THRESHOLD){
    isDragging = true;
    svgEl.setPointerCapture(panPointerId);
    svgEl.style.cursor = 'grabbing';
  }
  if(isDragging){
    const rect = svgEl.getBoundingClientRect();
    const factor = (VB_CX*2) / rect.width;
    panX = panStartX + dx * factor;
    panY = panStartY + dy * factor;
    applyMapZoom();
  }
});
function endDrag(e){
  if(panPointerId === null) return;
  if(e && e.pointerId !== panPointerId) return;
  if(isDragging) svgEl.releasePointerCapture(panPointerId);
  panPointerId = null;
  isDragging = false;
  svgEl.style.cursor = mapZoom > ZOOM_MIN ? 'grab' : 'default';
}
svgEl.addEventListener('pointerup', endDrag);
svgEl.addEventListener('pointerleave', endDrag);

applyMapZoom();


// Floating inline validation: only exact prefecture names are accepted.
function showPrefPrompt(input, message){
  let prompt = input.parentElement.querySelector('.pref-validation-prompt');
  if(!prompt){ prompt=document.createElement('div'); prompt.className='pref-validation-prompt'; prompt.setAttribute('role','status'); input.parentElement.appendChild(prompt); }
  prompt.textContent=message; prompt.hidden=false;
  input.setAttribute('aria-invalid','true');
}
function clearPrefPrompt(input){
  const prompt=input.parentElement.querySelector('.pref-validation-prompt');
  if(prompt) prompt.hidden=true;
  input.removeAttribute('aria-invalid');
}

/* ---------------- Prefecture search ---------------- */
const prefList = document.getElementById('pref-list');
Object.entries(PREFS).forEach(([id,p])=>{
  const opt = document.createElement('option');
  opt.value = p.name;
  prefList.appendChild(opt);
});
document.getElementById('check-risk-btn').addEventListener('click', ()=>{
  const input = document.getElementById('loc-input');
  const val = input.value.trim().toLowerCase();
  const match = Object.entries(PREFS).find(([id,p]) => p.name.toLowerCase() === val);
  if(!match){
    alert(val ? 'No exact match — please choose a Japanese prefecture.' : 'Please enter a prefecture name.');
    input.focus();
    return;
  }
  // Reads the live From/To values now. Nothing is applied unless both dates are valid.
  const period = readValidatedPeriod();
  if(!period) return;
  applyRiskContext(match[0], period);
});

// One validated context (prefecture + period) is applied in a single place, so every
// section below uses the same selection.
function readValidatedPeriod(){
  if(!validateDateRange(true)) return null;
  const from = fromDateInput.value;
  const to = toDateInput.value;
  return {from, to, months: monthIndexesForRange(from, to)};
}
function applyRiskContext(prefId, period){
  activePeriod = period;
  Object.keys(chartViews).forEach(key=>delete chartViews[key]);
  selectPref(prefId); // also refreshes the period summary and the hazard cards
  chartPref = prefId;
  const region=document.getElementById('region-select');
  if(region) region.value=prefId;
  renderCharts();
}

/* ---------------- Select prefecture ---------------- */
function modeledRiskScore(pref){
  return Math.max(...Object.entries(pref.hazards).filter(([key])=>key !== 'snow' || SNOW_MODEL_PREFECTURES.has(Object.keys(PREFS).find(id=>PREFS[id]===pref))).map(([,value])=>value));
}
function mapRiskColor(score){
  if(score < 25) return '#22C55E';
  if(score < 45) return '#F59E0B';
  return '#EF4444';
}
function updateMapChoropleth(){
  const selector = document.getElementById('map-hazard-select');
  if(selector){
    const snowOption = selector.querySelector('option[value="snow"]');
    if(snowOption) snowOption.hidden = !SNOW_MODEL_PREFECTURES.has(currentPref);
    if(selectedMapHazard === 'snow' && !SNOW_MODEL_PREFECTURES.has(currentPref)) selectedMapHazard = 'typhoon';
    selector.value = selectedMapHazard;
  }
  const hazardMeta = [
    {key:'typhoon', label:'Typhoon'},
    {key:'rain', label:'Heavy rain'},
    {key:'flood', label:'Flood'},
    {key:'landslide', label:'Landslide'},
    {key:'thunder', label:'Thunderstorm'},
    {key:'snow', label:'Heavy snow'}
  ].find(h=>h.key===selectedMapHazard);
  const legendTitle = document.getElementById('map-legend-title');
  if(legendTitle) legendTitle.textContent = (hazardMeta?.label || 'Disaster') + ' risk';
  document.querySelectorAll('.pref').forEach(el=>{
    const p = PREFS[el.dataset.id];
    if(p){
      const selected = el.dataset.id === currentPref;
      const darkMap = document.documentElement.getAttribute('data-theme') === 'dark';
      el.style.fill = selected ? '#2563EB' : '#9AAFC4';
      el.style.opacity = selected ? '1' : '.18';
      el.style.strokeWidth = selected ? '1.4' : '1';
      el.style.stroke = selected ? (darkMap ? '#BFDBFE' : '#1D4ED8') : (darkMap ? '#26384B' : '#FFFFFF');
      el.style.filter = selected ? 'drop-shadow(0 0 3px rgba(37,99,235,.65))' : 'none';
    }
  });
}
function zoomToPrefecture(id){
  const path = document.querySelector('.pref[data-id="' + id + '"]');
  if(!path || typeof path.getBBox !== 'function') return;
  const box = path.getBBox();
  if(!box.width || !box.height) return;
  const cx = box.x + box.width / 2;
  const cy = box.y + box.height / 2;
  const desired = Math.min(ZOOM_MAX, Math.max(2.0, Math.min(3.1, 150 / Math.max(box.width, box.height))));
  mapZoom = desired;
  panX = mapZoom * (VB_CX - cx);
  panY = mapZoom * (VB_CY - cy);
  applyMapZoom();
}
const mapHazardSelect = document.getElementById('map-hazard-select');
mapHazardSelect?.addEventListener('change', ()=>{
  selectedMapHazard = mapHazardSelect.value;
  if(selectedMapHazard === 'snow' && !SNOW_MODEL_PREFECTURES.has(currentPref)){
    selectedMapHazard = 'typhoon';
    mapHazardSelect.value = selectedMapHazard;
  }
  updateMapChoropleth();
  selectPref(currentPref, {zoom:false});
});
function selectPref(id, options = {}){
  if(selectedMapHazard === 'snow' && !SNOW_MODEL_PREFECTURES.has(id)) selectedMapHazard = 'typhoon';
  currentPref = id;
  chartPref = id;
  const p = PREFS[id];
  const clim = CLIMATE[p.archetype];
  const scores = hazardScoresFor(id);
  const eligibleSummaryHazards = HAZARD_META.filter(h=>h.key !== 'snow' || SNOW_MODEL_PREFECTURES.has(id));
  const topHazardForSummary = eligibleSummaryHazards.reduce((best,h)=>scores[h.key] > scores[best.key] ? h : best, eligibleSummaryHazards[0]);
  document.getElementById('map-summary-name').textContent = p.name;
  const overallRisk = levelFor(scores[topHazardForSummary.key]);
  document.getElementById('map-summary-hazard').textContent = overallRisk.label;
  document.getElementById('map-risk-summary').setAttribute('aria-label', \`\${p.name}: overall risk level \${overallRisk.label}.\`);

  document.querySelectorAll('.pref').forEach(el=> {
    const selected = el.dataset.id===id;
    el.classList.toggle('active', selected);
    el.setAttribute('aria-pressed', String(selected));
    const darkMap = document.documentElement.getAttribute('data-theme')==='dark';
    el.style.fill = selected ? '#2563EB' : '#9AAFC4';
    el.style.opacity = selected ? '1' : '.18';
    el.style.strokeWidth = selected ? '1.4' : '1';
    el.style.stroke = selected ? (darkMap ? '#BFDBFE' : '#1D4ED8') : (darkMap ? '#26384B' : '#FFFFFF');
    el.style.filter = selected ? 'drop-shadow(0 0 3px rgba(37,99,235,.65))' : 'none';
  });
  document.querySelectorAll('.pref-label').forEach(el=> {
    const selected = el.dataset.for===id;
    el.classList.toggle('active', selected);
    el.style.opacity = selected ? '1' : '.18';
  });
  document.getElementById('loc-input').value = p.name;

  document.getElementById('mon-loc').innerHTML = \`Monitoring temperature for <strong>\${p.name}</strong>\`;
  document.getElementById('stat-temp').textContent = clim.temp;




  const grid = document.getElementById('hazard-grid');
  grid.innerHTML = '';
  HAZARD_META.filter(h=>h.key !== 'snow' || SNOW_MODEL_PREFECTURES.has(id)).forEach(h=>{
    const pct = scores[h.key];
    const l = levelFor(pct);
    const el = document.createElement('div');
    el.className = 'card hazard';
    el.innerHTML = \`
      <div class="hazard-top">
        <span class="hazard-name">\${h.icon} \${h.label}</span>
        <span class="hazard-level \${l.cls}">\${l.label}</span>
      </div>
      <div class="bar-track"><div class="bar-fill" style="width:\${pct}%; background:\${l.color}"></div></div>
    \`;
    grid.appendChild(el);
  });

  document.getElementById('shelter-region').textContent = p.name;
  renderPlacesAndShelters(id);


  const regionSelect = document.getElementById('region-select');
  if(regionSelect) regionSelect.value = id;
  updateMapChoropleth();
  renderPeriodSummary(id);
  // Keep the full Japan map in view; users can zoom manually with the map controls.
}

/* ---------------- Places / shelters render (whole prefecture, no town filter) ---------------- */
function renderPlacesAndShelters(id){
  const p = PREFS[id];

  const shelterList = document.getElementById('shelter-list');
  shelterList.innerHTML = '';
  p.shelters.forEach((s,i)=>{
    const routeId = 'route-'+id+'-'+i;
    const h = hashStr(s.name);
    const dist = (0.3 + (h % 28) / 10).toFixed(1);
    const mins = 4 + (h % 22);
    const streets = ['Chuo-dori','Sakura-dori','Ekimae-dori','Honmachi-suji','Midori-dori'];
    const street = streets[h % streets.length];
    const el = document.createElement('div');
    el.className = 'shelter';
    el.innerHTML = \`
      <div class="name">\${s.name}</div>
      <div class="jp">\${s.jp}</div>
      <div class="note">\${s.note}</div>
      <div class="loc">\\ud83d\\udccd \${s.loc}</div>
      <button class="route-toggle" data-target="\${routeId}">Show directions \\u2192</button>
      <div class="route-panel" id="\${routeId}">
        <svg viewBox="0 0 200 56">
          <line x1="24" y1="28" x2="176" y2="28" stroke="#DDE3EA" stroke-width="3" stroke-dasharray="5,5"/>
          <circle cx="24" cy="28" r="7" fill="#3D8B8B"/>
          <text x="24" y="46" font-size="8" fill="#5C6674" text-anchor="middle">You</text>
          <circle cx="176" cy="28" r="7" fill="#E8A33D"/>
          <text x="176" y="46" font-size="8" fill="#5C6674" text-anchor="middle">Shelter</text>
        </svg>
        <div class="route-meta"><strong>\${dist} km</strong> \\u00b7 ~\${mins} min walk via \${street} (illustrative route)</div>
      </div>
    \`;
    shelterList.appendChild(el);
  });
  shelterList.querySelectorAll('.route-toggle').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      document.getElementById(btn.dataset.target).classList.toggle('open');
    });
  });

  const placeList = document.getElementById('place-list');
  placeList.innerHTML = '';
  p.places.forEach(pl=>{
    const el = document.createElement('div');
    el.className = 'place';
    el.setAttribute('role','button');
    el.setAttribute('tabindex','0');
    el.setAttribute('aria-expanded','false');
    el.innerHTML = \`
      <div class="name">\${pl.name}</div>
      <div class="jp">\${pl.jp}</div>
      <div class="note">\${pl.note}</div>
      <div class="loc">\\ud83d\\udccd \${pl.loc}</div>
      <div class="nearest">\\ud83c\\udfeb Nearest evacuation shelter: <strong>\${pl.nearest}</strong></div>
    \`;
    const togglePlace = ()=>{
      const expanded = el.classList.toggle('expanded');
      el.setAttribute('aria-expanded', String(expanded));
    };
    el.addEventListener('click', togglePlace);
    el.addEventListener('keydown', event=>{
      if(event.key==='Enter' || event.key===' '){ event.preventDefault(); togglePlace(); }
    });
    placeList.appendChild(el);
  });

  const subEl = document.getElementById('pane-sub');
  const activeMode = document.querySelector('.toggle-btn.active')?.dataset.mode || 'places';
  subEl.textContent = activeMode==='places'
    ? 'Tourist spots in this prefecture. Tap one to see its nearest evacuation shelter.'
    : 'All designated evacuation shelters for this prefecture.';
}

/* ---------------- Places / shelters toggle ---------------- */
document.querySelectorAll('.toggle-btn').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    document.querySelectorAll('.toggle-btn').forEach(b=>{
      b.classList.toggle('active', b===btn);
      b.setAttribute('aria-selected', b===btn);
    });
    const mode = btn.dataset.mode;
    document.getElementById('place-list').style.display = mode==='places' ? '' : 'none';
    document.getElementById('shelter-list').style.display = mode==='shelters' ? '' : 'none';
    renderPlacesAndShelters(currentPref);
  });
});

/* ---------------- Data viz region select ---------------- */
const regionSelect = document.getElementById('region-select');
const archOrder = ['hokkaido','tohoku','kanto','chubu','kansai','chugoku','shikoku','kyushu','okinawa'];
archOrder.forEach(arch=>{
  const group = document.createElement('optgroup');
  group.label = ARCH_LABELS[arch];
  Object.entries(PREFS).filter(([id,p])=>p.archetype===arch).forEach(([id,p])=>{
    const opt = document.createElement('option');
    opt.value = id; opt.textContent = p.name;
    group.appendChild(opt);
  });
  regionSelect.appendChild(group);
});
regionSelect.value = currentPref;
regionSelect.addEventListener('change', ()=>{
  chartPref = regionSelect.value;
  renderCharts();
});

const chartViews = {};
// Visible chart window over the active months. The window is a run of positions in
// that list, so a multi-year range (e.g. Nov, Dec, Jan, Feb) zooms like a normal one.
function visibleWindowFor(id){
  const months = activeMonthIndexes();
  const stored = chartViews[id];
  if(!stored) return {months, start:0, count:months.length};
  const count = Math.max(Math.min(3, months.length), Math.min(months.length, stored.count));
  const start = Math.max(0, Math.min(months.length - count, stored.start));
  return {months, start, count};
}
function changeChartZoom(id, action){
  const state = visibleWindowFor(id);
  const total = state.months.length;
  if(action==='reset') chartViews[id]={start:0,count:total};
  else {
    const nextCount=action==='in' ? Math.max(Math.min(3,total),state.count-2) : Math.min(total,state.count+2);
    const center=state.start+state.count/2;
    const nextStart=Math.max(0,Math.min(total-nextCount,Math.round(center-nextCount/2)));
    chartViews[id]={start:nextStart,count:nextCount};
  }
  renderCharts();
}
document.addEventListener('click', event=>{
  const btn=event.target.closest('[data-chart-action][data-chart-id]');
  if(btn) changeChartZoom(btn.dataset.chartId, btn.dataset.chartAction);
});

function chartBase(){
  const d3 = window.d3;
  if(!d3) return;
  const styles = getComputedStyle(document.documentElement);
  const read = name => styles.getPropertyValue(name).trim();
  const colors = {
    text: read('--chart-text') || '#334155',
    grid: read('--chart-grid') || '#D8E0E8',
    axis: read('--chart-axis') || '#8793A3',
    blue: read('--chart-blue') || '#2563EB',
    teal: read('--chart-teal') || '#0F766E',
    orange: read('--chart-orange') || '#C2410C',
    purple: read('--chart-purple') || '#7C3AED',
    red: read('--chart-red') || '#B91C1C',
    surface: read('--surface') || '#FFFFFF'
  };
  return { d3, colors };
}

function drawD3Chart(id, data, type, color, label){
  const base = chartBase();
  if(!base) return;
  const { d3, colors } = base;
  const container = document.getElementById(id);
  if(!container) return;
  container.replaceChildren();
  const width = Math.max(280, container.clientWidth || 520);
  const height = Math.max(190, container.clientHeight || 220);
  const margin = {top:14, right:14, bottom:36, left:44};
  const innerW = width - margin.left - margin.right;
  const innerH = height - margin.top - margin.bottom;
  const svg = d3.select(container).append('svg')
    .attr('viewBox', \`0 0 \${width} \${height}\`)
    .attr('role','img')
    .attr('aria-label', \`\${label}. Monthly illustrative scores from 0 to 100.\`);
  svg.append('title').text(\`\${label} — \${PREFS[chartPref].name}\`);
  const g = svg.append('g').attr('transform', \`translate(\${margin.left},\${margin.top})\`);
  const view = visibleWindowFor(id);
  const visibleIdx = view.months.slice(view.start, view.start + view.count);
  const visibleMonths = visibleIdx.map(i=>MONTHS[i]);
  const visibleData = visibleIdx.map(i=>data[i]);
  const x = d3.scaleBand().domain(visibleMonths).range([0,innerW]).padding(type==='bar' ? .2 : .05);
  // Keep Y fixed at 0–100; zoom only changes the visible X-axis months.
  const y = d3.scaleLinear().domain([0,100]).range([innerH,0]);
  g.append('g').attr('class','grid').call(d3.axisLeft(y).ticks(5).tickSize(-innerW).tickFormat(()=> ''));
  g.selectAll('.grid line').attr('stroke',colors.grid);
  g.append('g').attr('class','axis').attr('transform',\`translate(0,\${innerH})\`).call(d3.axisBottom(x).tickSizeOuter(0));
  g.append('g').attr('class','axis').call(d3.axisLeft(y).ticks(5).tickSizeOuter(0).tickPadding(7));
  if(type==='bar'){
    g.selectAll('rect.bar').data(visibleData).join('rect')
      .attr('class','bar').attr('x',(d,i)=>x(visibleMonths[i]))
      .attr('y',d=>y(d)).attr('width',x.bandwidth()).attr('height',d=>innerH-y(d))
      .attr('rx',3).attr('fill',d=>d>=45?colors.orange:color)
      .append('title').text((d,i)=>\`\${visibleMonths[i]}: \${d}/100 (illustrative score)\`);
  } else {
    const line = d3.line().x((d,i)=>x(visibleMonths[i])+x.bandwidth()/2).y(d=>y(d)).curve(d3.curveMonotoneX);
    const area = d3.area().x((d,i)=>x(visibleMonths[i])+x.bandwidth()/2).y0(innerH).y1(d=>y(d)).curve(d3.curveMonotoneX);
    g.append('path').datum(visibleData).attr('d',area).attr('fill',color).attr('opacity',.12);
    g.append('path').datum(visibleData).attr('d',line).attr('fill','none').attr('stroke',color).attr('stroke-width',2.5);
    g.selectAll('circle.point').data(visibleData).join('circle').attr('class','point')
      .attr('cx',(d,i)=>x(visibleMonths[i])+x.bandwidth()/2).attr('cy',d=>y(d)).attr('r',3.3)
      .attr('fill',color).attr('stroke',colors.surface).attr('stroke-width',1.2)
      .append('title').text((d,i)=>\`\${visibleMonths[i]}: \${d}/100 (illustrative score)\`);
  }
  document.querySelectorAll('[data-chart-id="'+id+'" ]').forEach(btn=>{
    btn.disabled = btn.dataset.chartAction==='in' ? view.count<=Math.min(3,view.months.length) : btn.dataset.chartAction==='out' ? view.count>=view.months.length : false;
  });
  g.selectAll('.axis text').attr('fill',colors.text);
  g.selectAll('.axis path,.axis line').attr('stroke',colors.axis);
  g.selectAll('.grid path').attr('display','none');
}

function renderCharts(){
  const p = PREFS[chartPref];
  const snowCard = document.getElementById('chart-snow')?.closest('.chart-card');
  if(snowCard) snowCard.hidden = !SNOW_MODEL_PREFECTURES.has(chartPref);
  const m = p.monthly;
  const palette = chartBase()?.colors;
  if(!palette) return;
  drawD3Chart('chart-bar', m.disruption, 'bar', palette.teal, 'Overall monthly disruption score');
  drawD3Chart('chart-typhoon', m.typhoon, 'line', palette.red, 'Typhoon seasonality');
  drawD3Chart('chart-flood', m.flood, 'line', palette.teal, 'Heavy rain and flood risk');
  drawD3Chart('chart-landslide', m.landslide, 'line', palette.purple, 'Landslide and mudslide risk');
  drawD3Chart('chart-snow', m.snow, 'line', palette.blue, 'Heavy snow risk');
}
window.addEventListener('resize', ()=>{
  if(document.getElementById('view-dataviz')?.classList.contains('active')) renderCharts();
});

/* ---------------- Home quick search and accessibility controls ---------------- */
const homePrefList = document.getElementById('home-pref-list');
Object.values(PREFS).forEach(p=>{
  const option = document.createElement('option');
  option.value = p.name;
  homePrefList.appendChild(option);
});
function runHomeSearch(){
  const value = document.getElementById('home-pref-search').value.trim().toLowerCase();
  const match = Object.entries(PREFS).find(([id,p])=>p.name.toLowerCase()===value);
  if(match){
    selectPref(match[0]);
    switchView('prediction');
    document.getElementById('loc-input').value = match[1].name;
    document.getElementById('map-risk-summary').scrollIntoView({behavior:document.body.classList.contains('access-reduce-motion')?'auto':'smooth',block:'start'});
  } else if(value) {
    showPrefPrompt(document.getElementById('home-pref-search'),'Please enter a valid Japanese prefecture name.');
  }
}
document.getElementById('home-search-btn').addEventListener('click',runHomeSearch);
document.getElementById('home-pref-search').addEventListener('keydown',e=>{if(e.key==='Enter')runHomeSearch();});
document.getElementById('home-pref-search').addEventListener('input',e=>clearPrefPrompt(e.target));
document.getElementById('loc-input').addEventListener('input',e=>clearPrefPrompt(e.target));
function setAccessibility(kind, enabled){
  const className = kind==='larger'?'access-large':kind==='contrast'?'access-contrast':'access-reduce-motion';
  document.body.classList.toggle(className, enabled);
  document.querySelectorAll('[data-access="'+kind+'"]').forEach(btn=>{
    btn.setAttribute('aria-pressed', String(enabled));
    const label=kind==='larger'?'Larger text':kind==='contrast'?'High contrast':'Reduced motion';
    btn.setAttribute('aria-label', label + ' ' + (enabled?'enabled':'disabled'));
  });
  try { localStorage.setItem('kikan-access-'+kind, String(enabled)); } catch(e) {}
}
['larger','contrast','motion'].forEach(kind=>{
  let enabled = false;
  try { enabled = localStorage.getItem('kikan-access-'+kind) === 'true'; } catch(e) {}
  setAccessibility(kind, enabled);
});
document.querySelectorAll('[data-access]').forEach(btn=>{
  btn.addEventListener('click',()=>{
    const kind=btn.dataset.access;
    const className=kind==='larger'?'access-large':kind==='contrast'?'access-contrast':'access-reduce-motion';
    setAccessibility(kind, !document.body.classList.contains(className));
  });
});
updateMapChoropleth();

/* ---------------- init ---------------- */
/* single Safety tips panel (next to the section heading) */
document.getElementById('tips-btn').addEventListener('click', ()=>{
  const btn = document.getElementById('tips-btn');
  const panel = document.getElementById('tips-panel');
  const open = btn.getAttribute('aria-expanded') === 'true';
  btn.setAttribute('aria-expanded', String(!open));
  panel.hidden = open;
});

// Date handling. Dates are YYYY-MM-DD strings, compared as strings and never converted
// to Date objects or timestamps. "Today" is the current calendar date in Japan.
const fromDateInput = document.getElementById('from-date');
const toDateInput = document.getElementById('to-date');
const dateRangeError = document.createElement('p');
dateRangeError.id = 'date-range-error';
dateRangeError.className = 'date-range-error';
dateRangeError.hidden = true;
dateRangeError.setAttribute('role', 'alert');
document.getElementById('check-risk-btn')?.insertAdjacentElement('afterend', dateRangeError);

const MAX_ALLOWED_DATE = '2027-12-31';
const DATE_RANGE_MESSAGE = 'Select valid From and To dates from today through 31 December 2027 (Japan time).';
const DATE_ORDER_MESSAGE = 'The To date must be on or after the From date.';
const FROM_DATE_MESSAGE = 'Choose a From date from today through 31 December 2027 (Japan time).';
const TO_DATE_MESSAGE = 'Choose a To date on or after the From date, no later than 31 December 2027.';

function getJapanTodayISO(){
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Tokyo', year: 'numeric', month: '2-digit', day: '2-digit'
  }).formatToParts(new Date());
  const part = type => parts.find(item => item.type === type)?.value || '';
  return part('year') + '-' + part('month') + '-' + part('day');
}
function daysInMonth(year, month){
  if(month === 2) return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0 ? 29 : 28;
  return [4, 6, 9, 11].includes(month) ? 30 : 31;
}
// Checks the shape and calendar validity of a YYYY-MM-DD string using only numbers.
function isCalendarDate(value){
  if(typeof value !== 'string' || !/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/.test(value)) return false;
  const year = Number(value.slice(0, 4));
  const month = Number(value.slice(5, 7));
  const day = Number(value.slice(8, 10));
  return month >= 1 && month <= 12 && day >= 1 && day <= daysInMonth(year, month);
}
function isAllowedDate(value){
  return isCalendarDate(value) && value >= getJapanTodayISO() && value <= MAX_ALLOWED_DATE;
}
function formatDateLabel(iso){
  return Number(iso.slice(8, 10)) + ' ' + MONTHS[Number(iso.slice(5, 7)) - 1] + ' ' + iso.slice(0, 4);
}
function refreshDateConstraints(){
  if(!fromDateInput || !toDateInput) return;
  const todayJapan = getJapanTodayISO();
  fromDateInput.min = todayJapan;
  fromDateInput.max = MAX_ALLOWED_DATE;
  const earliestToDate = fromDateInput.value && isAllowedDate(fromDateInput.value)
    ? (fromDateInput.value > todayJapan ? fromDateInput.value : todayJapan)
    : todayJapan;
  toDateInput.min = earliestToDate;
  toDateInput.max = MAX_ALLOWED_DATE;
}
// showMessage=true (Check risk) shows the inline message and focuses the bad field.
// showMessage=false (typing) only updates the field validity and never shows a prompt.
function validateDateRange(showMessage = false){
  if(!fromDateInput || !toDateInput) return false;
  refreshDateConstraints();
  const fromValue = fromDateInput.value;
  const toValue = toDateInput.value;
  const fromValid = isAllowedDate(fromValue);
  const toValid = isAllowedDate(toValue);
  const orderValid = fromValid && toValid && toValue >= fromValue;
  const ok = fromValid && toValid && orderValid;
  fromDateInput.setCustomValidity(fromValid ? '' : FROM_DATE_MESSAGE);
  toDateInput.setCustomValidity(toValid && orderValid ? '' : TO_DATE_MESSAGE);
  if(showMessage){
    dateRangeError.textContent = ok ? '' : (fromValid && toValid ? DATE_ORDER_MESSAGE : DATE_RANGE_MESSAGE);
    dateRangeError.hidden = ok;
    if(!ok) (fromValid ? toDateInput : fromDateInput).reportValidity();
  } else if(ok){
    dateRangeError.hidden = true;
  }
  return ok;
}

// Calendar months covered by a validated range, in chronological order. Ranges may span
// years: 2026-11-15 to 2027-02-15 gives Nov, Dec, Jan, Feb (indexes 10, 11, 0, 1).
function monthIndexesForRange(from, to){
  const start = Number(from.slice(0, 4)) * 12 + Number(from.slice(5, 7)) - 1;
  const end = Number(to.slice(0, 4)) * 12 + Number(to.slice(5, 7)) - 1;
  const indexes = [];
  for(let k = start; k <= end && indexes.length < 12; k++){
    const month = k % 12;
    if(!indexes.includes(month)) indexes.push(month);
  }
  return indexes;
}
function activeMonthIndexes(){
  return activePeriod ? activePeriod.months : MONTHS.map((_, i) => i);
}
// Hazards with bundled monthly series. With an applied period they show the highest
// monthly score inside the period. Other hazards keep their static prefecture value.
const PERIOD_HAZARD_KEYS = ['typhoon', 'flood', 'landslide', 'snow'];
function hazardScoresFor(id){
  const p = PREFS[id];
  if(!activePeriod) return p.hazards;
  const scores = {...p.hazards};
  PERIOD_HAZARD_KEYS.forEach(key=>{
    const series = p.monthly?.[key];
    if(Array.isArray(series)) scores[key] = Math.max(...activePeriod.months.map(i=>series[i]));
  });
  return scores;
}
// Prototype summary under the monitoring card. Built from the same hazard scores the
// cards use, so it always matches them. Shows "full year" when no Check risk period is applied.
function renderPeriodSummary(id){
  const summary = document.getElementById('monitor-risk-summary');
  if(!summary) return;
  const p = PREFS[id];
  const scores = hazardScoresFor(id);
  const months = activeMonthIndexes();
  const eligible = HAZARD_META.filter(h=>h.key !== 'snow' || SNOW_MODEL_PREFECTURES.has(id));
  const top = eligible.reduce((best,h)=>scores[h.key] > scores[best.key] ? h : best, eligible[0]);
  const level = levelFor(scores[top.key]).label;
  const series = p.monthly?.[top.key];
  let peak = '';
  if(Array.isArray(series)){
    const peakIdx = months.reduce((best,i)=>series[i] > series[best] ? i : best, months[0]);
    peak = ', peaking in ' + MONTHS[peakIdx];
  }
  const period = activePeriod
    ? ', ' + formatDateLabel(activePeriod.from) + ' – ' + formatDateLabel(activePeriod.to)
    : ' (full year)';
  summary.textContent = 'Prototype summary for ' + p.name + period + ': the highest illustrative score is ' + top.label + ' (' + level + ')' + peak + '. Check official local alerts before travel. These are illustrative values, not live warnings.';
}

[fromDateInput, toDateInput].forEach(input => {
  if(!input) return;
  input.addEventListener('input', () => validateDateRange(false));
  input.addEventListener('change', () => validateDateRange(false));
});
refreshDateConstraints();

selectPref('tokyo');
`;

