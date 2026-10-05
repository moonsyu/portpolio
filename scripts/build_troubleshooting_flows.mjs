// Source-grounded explanatory flowcharts; historical evidence is indexed in docs.
import { mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const out = fileURLToPath(new URL('../assets/flows/', import.meta.url));
mkdirSync(out, {recursive:true});
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
function chart(name,title,w,h,draw){
 let parts=[`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-labelledby="title"><title id="title">${esc(title)}</title><defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 Z" fill="#2355de"/></marker></defs><rect width="${w}" height="${h}" fill="white"/><style>text{font-family:'Malgun Gothic','Segoe UI',sans-serif;fill:#172538;font-weight:650}.note{fill:#526780}.heading{fill:#2355de;font-weight:750}.edge{fill:none;stroke:#2355de;stroke-width:2.5;marker-end:url(#arrow)}</style>`];
 const text=(x,y,lines,size=26,cls='')=>parts.push(`<text x="${x}" y="${y}" text-anchor="middle" class="${cls}" font-size="${size}">${lines.map((l,i)=>`<tspan x="${x}" dy="${i?size*1.45:0}">${esc(l)}</tspan>`).join('')}</text>`);
 const node=(x,y,ww,hh,lines,{round=false,fill='#f8fafc',size=26}={})=>{parts.push(`<rect x="${x}" y="${y}" width="${ww}" height="${hh}" rx="${round?hh/2:10}" fill="${fill}" stroke="#c5d2e6" stroke-width="2"/>`);text(x+ww/2,y+hh/2-(lines.length-1)*size*.72+size*.35,lines,size);};
 const diamond=(x,y,ww,hh,lines)=>{parts.push(`<path d="M${x+ww/2} ${y} L${x+ww} ${y+hh/2} L${x+ww/2} ${y+hh} L${x} ${y+hh/2} Z" fill="#eef3ff" stroke="#2355de" stroke-width="2"/>`);text(x+ww/2,y+hh/2-(lines.length-1)*19+9,lines,25);};
 const edge=(d)=>parts.push(`<path class="edge" d="${d}"/>`);
 const line=(x1,y1,x2,y2)=>edge(`M${x1} ${y1} L${x2} ${y2}`);
 draw({text,node,diamond,edge,line,parts});
 parts.push('</svg>');writeFileSync(out+name+'.svg',parts.join('\n'));
}

chart('arabica-backup','Arabica: 백업 실행과 주기적 완료 확인 분리',960,1120,({text,node,diamond,edge,line,parts})=>{
 text(250,40,['변경 전 · 완료 대기'],29,'heading');text(250,76,['완료까지 Thread 점유'],23,'note');text(710,48,['변경 후 · 실행 / 확인 분리'],29,'heading');
 parts.push('<path d="M480 78 V1080" stroke="#dce3ed" stroke-width="2" stroke-dasharray="7 7"/>');
 node(90,100,320,78,['백업 스케줄 실행'],{round:true});line(250,178,250,218);
 node(90,218,320,96,['SSH 명령 호출','원격 Bash 실행']);line(250,314,250,354);
 diamond(90,354,320,144,['백업 종료?']);
 edge('M90 426 H40 V334 H250 V354');text(75,462,['대기'],23,'note');
 line(250,498,250,626);text(282,614,['예'],22,'note');
 node(90,626,320,82,['후속 처리'],{round:true});
 node(550,100,320,78,['백업 스케줄 실행'],{round:true});line(710,178,710,218);
 node(550,218,320,96,['별도 실행기 진입','@Async']);line(710,314,710,354);
 node(550,354,320,96,['원격 백그라운드 실행','nohup bash … &']);line(710,450,710,490);
 node(550,490,320,78,['실행 호출 반환'],{round:true});
 text(710,630,['별도 결과 확인 주기'],26,'heading');
 node(550,666,320,82,['5분 간격 확인','결과 파일 판독']);line(710,748,710,788);
 diamond(550,788,320,134,['완료 결과 존재?']);
 edge('M550 855 H510 V707 H550');text(557,779,['아니오'],19,'note');
 line(710,922,710,960);text(748,949,['예'],22,'note');
 node(550,960,320,106,['업로드·데이터 검증','완료 결과와 이력 저장']);
 text(250,806,['백업 실행과 결과 처리가','동일 대기 흐름에 연결'],23,'note');
});

chart('cmp-webflux','CMP: 외부 API 동기 응답 대기에서 WebFlux 응답 연결로 전환',960,930,({text,node,diamond,edge,line,parts})=>{
 text(245,40,['변경 전 · MVC 동기 호출'],28,'heading');text(245,76,['응답 대기 중 Thread 점유'],23,'note');text(720,48,['변경 후 · WebFlux'],28,'heading');
 parts.push('<path d="M480 78 V886" stroke="#dce3ed" stroke-width="2" stroke-dasharray="7 7"/>');
 for(const x of [245,720]){node(x-160,100,320,76,['클라이언트 요청'],{round:true});line(x,176,x,220);}
 node(85,220,320,96,['Controller · Service','외부 API 호출']);line(245,316,245,370);
 diamond(85,370,320,140,['응답 도착?']);
 edge('M85 440 H38 V342 H245 V370');text(70,479,['대기'],23,'note');
 line(245,510,245,658);text(282,638,['예'],22,'note');node(85,658,320,90,['응답 데이터 처리']);
 line(245,748,245,798);node(85,798,320,76,['클라이언트 응답'],{round:true});
 node(560,220,320,96,['WebClient 요청','Mono 처리 흐름 연결']);line(720,316,720,370);
 node(560,370,320,110,['외부 I/O 응답 대기','대기 Thread 점유 분리']);line(720,480,720,552);
 text(806,523,['응답 준비 알림'],21,'note');
 node(560,552,320,96,['Mono 후속 처리','응답 데이터 변환']);line(720,648,720,798);
 node(560,798,320,76,['클라이언트 응답'],{round:true});
});

chart('wallet-xss','Wallet: JSON의 정제값을 요청 본문에 반영하는 XSS 처리 흐름',940,1170,({text,node,diamond,edge,line})=>{
 text(470,48,['정제 결과를 요청 본문까지 전달'],30,'heading');
 node(285,92,370,76,['복호화된 JSON'],{round:true});line(470,168,470,210);
 node(285,210,370,92,['중첩 객체·배열 순회']);line(470,302,470,344);
 diamond(300,344,340,142,['문자열 값인가?']);
 edge('M300 415 H200 V535');text(237,400,['예'],23,'note');
 edge('M640 415 H755 V535');text(700,400,['아니오'],23,'note');
 node(40,535,320,100,['AntiSamy 정책 적용','정제 문자열 반환']);
 node(595,535,300,100,['숫자·불리언 등','비문자열 값 유지']);
 node(50,674,300,82,['원래 값을 정제값으로 교체'],{fill:'#eef3ff',size:23});line(200,635,200,674);
 edge('M200 756 V807 H470 V853');edge('M745 635 V807 H470 V853');
 node(285,853,370,92,['변경된 JSON으로','요청 본문 재구성']);line(470,945,470,988);
 node(285,988,370,76,['업무 API에 전달'],{round:true});
 text(470,1112,['정책 객체는 한 번 준비하고 재사용'],25,'note');
});
chart('store-migration','Store: 장바구니·결제 옵션의 FK를 부모 PK 참조로 변경',960,1050,({text,node,edge,parts})=>{
 text(240,45,['변경 전 · 비유일 컬럼 참조'],28,'heading');
 text(720,45,['변경 후 · 부모 PK 참조'],28,'heading');
 parts.push('<path d="M480 82 V1000" stroke="#dce3ed" stroke-width="2" stroke-dasharray="7 7"/>');
 for(const [y,title,parent] of [[120,'장바구니 옵션','장바구니 행'],[590,'결제 옵션','결제 상품 행']]){
  text(240,y-25,[title],25,'heading');text(720,y-25,[title],25,'heading');
  for(const x of [240,720]){
   node(x-180,y,360,72,[parent]);
   node(x-180,y+165,360,72,['옵션 그룹 연결 행']);
   node(x-180,y+330,360,72,['옵션 상세 연결 행']);
   edge(`M${x-145} ${y+165} V${y+72}`);
   edge(`M${x-145} ${y+330} V${y+237}`);
  }
  text(260,y+115,['상품 ID'],24);text(260,y+145,['중복 가능'],21,'note');
  text(260,y+280,['옵션 그룹 ID'],24);text(260,y+310,['중복 가능'],21,'note');
  text(740,y+124,[title==='장바구니 옵션'?'장바구니 PK':'결제 상품 연결 PK'],24);
  text(740,y+289,['옵션 그룹 연결 PK'],24);
 }
 text(480,1023,['자식 → 부모 참조 · 4개 관계의 참조 컬럼 교정'],24,'note');
});
console.log('Created 4 source-grounded flowcharts.');
