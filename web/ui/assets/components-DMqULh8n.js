import{r as k,d as S,a as L,c as u,o as n,F as j,b as T,e as f,n as b,w as I,f as e,g as J,h as U,i as V,j as B,T as R,u as g,v as Z,t as _,k as N,K as Q,l as W,m as X,p as O,q as P,s as M,x as Y,y as ee}from"./vendor-BjbVr-eA.js";import{u as G,a as te}from"./router-Bmv6I3vY.js";const le="/py-tosha-a.svg",q="/py-Tosha.svg",H="/ios_spin.svg",C="http://192.168.1.108/",v=k({}),se={class:"nav _nav_wrap d-md2-none"},ae=["src"],oe=S({__name:"Nav_Bar",setup($){const a=[{img:"/net_wifi.svg",to:"/network"},{img:"/folder_files.svg",to:"/files"},{img:"/info.svg",to:"/info"},{img:"/switches.svg",to:"/switches"},{img:"/schedule.svg",to:"/cron_scheduler"},{img:"/settings.svg",to:"/settings"}];return(i,o)=>{const p=L("router-link");return n(),u("nav",se,[(n(),u(j,null,T(a,y=>f(p,{class:b(["btn my-2 _mx-auto",{hilith:i.$route.path==y.to}]),to:y.to},{default:I(()=>[e("img",{src:y.img},null,8,ae)]),_:2},1032,["class","to"])),64))])}}}),D=($,a)=>{const i=$.__vccOpts||$;for(const[o,p]of a)i[o]=p;return i},ne=D(oe,[["__scopeId","data-v-be357fa7"]]),ie={class:"layout"},ce={key:"1",src:le,class:"ma-1",alt:"py-Tosha logo"},re={key:"2",src:q,class:"ma-1",alt:"py-Tosha logo"},ue={key:"2",src:q,class:"ma-1",alt:"py-Tosha logo"},de={key:"2",src:H,class:"ma-1",alt:"py-Tosha logo"},_e={class:"title text-h2"},ve={style:{"_padding-left":"50px"}},fe=S({__name:"LayoutDefault",setup($){let a=k(!0);const i=G();let o=k(!1);setTimeout(()=>o.value=!0,2222);const p=J(()=>{var t;return((t=v.value)==null?void 0:t.datetime)&&new Date(v.value.datetime).toISOString().slice(8,16).replace("T"," ")});let y=null;return U(()=>i.name,()=>{clearTimeout(y),y=setTimeout(()=>a.value=!1,7e3),!a.value&&setTimeout(()=>a.value=!0,400)}),(t,c)=>{const h=L("router-link"),w=L("router-view");return n(),u("div",ie,[e("header",null,[f(h,{to:"/",_target:"_blank",class:b(["logo",{home:t.$route.name!="home"}])},{default:I(()=>[f(R,{name:"fade"},{default:I(()=>[g(a)?(n(),u("img",ce)):(n(),u("img",re))]),_:1}),g(o)?V((n(),u("img",ue,null,512)),[[Z,!1]]):B("",!0)]),_:1},8,["class"]),g(o)?V((n(),u("img",de,null,512)),[[Z,!1]]):B("",!0),e("h2",_e,_(t.$route.meta.label||"py-Tosha"),1)]),e("main",ve,[f(ne),f(w,{class:"view"},{default:I(({Component:l})=>[f(R,{name:"pagefade","_before-enter":"over_hide=true",_enter:"onEnter","_after-enter":"over_hide=false","_enter-cancelled":"over_hide=false"},{default:I(()=>[(n(),N(Q,{max:"3"},[(n(),N(W(l),{class:"viewG"}))],1024))]),_:2},1024)]),_:1})]),e("footer",null,[e("ul",null,[e("li",{class:b({"bg-warn":g(v).err})},_(p.value),3),e("li",{class:b({"bg-warn":g(v).err})},"mem: "+_(~~(g(v).mem_free/100)/10)+"k",3),e("li",{class:b({"bg-warn":g(v).err})},"cpu: "+_(~~(g(v).load*100+1))+"%",3)])])])}}}),xt=D(fe,[["__scopeId","data-v-f61e1ae2"]]),pe={key:0,src:H},me={key:1,class:"mx-2"},he=S({__name:"ZButton",props:{to:{type:[Object,String],required:!1},label:{},ladge:{type:Boolean,default:!1},loading:{type:Boolean,default:!1}},setup($){return(a,i)=>{const o=L("router-link");return $.to?(n(),N(o,{key:0,class:b(["btn my-2 gggg _mx-auto",{ladge:$.ladge}]),to:$.to},{default:I(()=>[O(_($.label),1)]),_:1},8,["class","to"])):(n(),u("a",{key:1,class:b(["btn my-2 _mx-auto",{ladge:$.ladge}]),_to:"to"},[X(a.$slots,"prepend",{},void 0),$.loading?(n(),u("img",pe)):(n(),u("span",me,_($.label),1))],2))}}}),m=D(he,[["__scopeId","data-v-c810bab2"]]),ge={class:"wrapper"},ye={class:"d-flex_"},be=S({__name:"home",setup($){return(a,i)=>(n(),u("div",ge,[e("div",ye,[e("div",null,[f(m,{ladge:"",to:"/network",label:"network"})]),e("div",null,[f(m,{ladge:"",to:"/files",label:"files"})]),e("div",null,[f(m,{ladge:"",to:"/info",label:"info"})]),e("div",null,[f(m,{ladge:"",to:"/switches",label:"switches"})]),e("div",null,[f(m,{ladge:"",to:"/cron_scheduler",label:"scheduler"})]),e("div",null,[f(m,{ladge:"",to:"/settings",label:"settings"})])])]))}}),$e=D(be,[["__scopeId","data-v-da30073d"]]),Ct=Object.freeze(Object.defineProperty({__proto__:null,default:$e},Symbol.toStringTag,{value:"Module"})),we={class:"row pa-2"},ke={class:"row pa-2"},xe={class:"col-md-12 _col-4 px-2 text-b"},Ce={class:"col-md-12 col-8 px-2"},Se={key:0,style:{"justify-items":"left"}},je={class:"txt-left"},Te={key:1},Oe=S({__name:"info",setup($){const a=k(null);let i=null;function o(){fetch(`${C}api/status`).then(async t=>{if(t.ok){const c=await t.json();a.value=c}else a.value=[]}).catch(t=>a.value=[])}const p=J(()=>{var t;return((t=v.value)==null?void 0:t.datetime)&&new Date(v.value.datetime).toISOString().slice(8,16).replace("T"," ")});function y(){o()}return P(()=>{i=!0,o()}),M(()=>{i=!1}),U(()=>v.value.err,t=>{!t&&i&&o()}),(t,c)=>(n(),u("div",null,[c[1]||(c[1]=e("h3",null,"Информация",-1)),f(m,{onClick:c[0]||(c[0]=h=>t.$router.go(-1)),label:"<<",class:"mx-2"}),f(m,{onClick:y,label:"refresh"}),e("div",we,[e("div",{class:b(["col-3 col-sm-6 pa-2 justify-cc",{"bg-warn":g(v).err}])}," PLC time: "+_(p.value),3),e("div",{class:b(["col-3 col-sm-6 pa-2 justify-cc",{"bg-warn":g(v).err}])},"Free mem: "+_(~~(g(v).mem_free/100)/10)+"k",3),e("div",{class:b(["col-3 col-sm-6 pa-2 justify-cc",{"bg-warn":g(v).err}])},"UpTime: "+_(~~(g(v).uptime/60))+"min",3),e("div",{class:b(["col-3 col-sm-6 pa-2 justify-cc",{"bg-warn":g(v).err}])},"CPU load: "+_(~~(g(v).load*100+1))+"%",3)]),(n(!0),u(j,null,T(a.value,(h,w)=>(n(),u("div",ke,[e("div",xe,_(h.name),1),e("div",Ce,[Array.isArray(h.state)?(n(),u("div",Se,[(n(!0),u(j,null,T(h.state,l=>(n(),u("div",je,_(l),1))),256))])):(n(),u("div",Te,_(h.state),1))])]))),256))]))}}),St=Object.freeze(Object.defineProperty({__proto__:null,default:Oe},Symbol.toStringTag,{value:"Module"})),Ie={class:"row px-2"},Pe={class:"list_files col-8 col-sm-12"},De={class:"col-12 ma-2"},Ne={class:"ant mx-2"},ze=["onClick"],Be=S({__name:"network",setup($){const a=k([]),i=k(""),o=k(!1);let p=0,y;function t(){o.value||(o.value=!0,fetch(`${C}api/net/scan`).then(async l=>{if(l.ok){const r=await l.json();i.value=r.connected,a.value=a.value.filter(s=>!r.available.find(d=>s[1]==d[1])&&s[6]+6>~~(Date.now()/1e3/60)),a.value.push(...r.available.map(s=>(s[0]=s[0]||s[1],s[6]=~~(Date.now()/1e3/60),s))),a.value=a.value.sort((s,d)=>s[3]>d[3]?-1:s[3]<d[3]?1:0)}}).finally(()=>{o.value=!1,!(p>3)&&(p++,y=setTimeout(t,(.5+p/3)*60*1e3))}))}function c(){if(!o.value&&confirm("Подтвердите действие - забыть сеть")){o.value=!0;const l={method:"delete"};fetch(`${C}api/net/config`,l).then(async r=>{r.ok&&(i.value="")}).finally(()=>{o.value=!1})}}function h(l){if(o.value)return;const r=prompt(`Введите ключ подключения к сетти ${l}`,"");if(r){o.value=!0;const s={method:"post",body:JSON.stringify({ssid:l,pswd:r})};fetch(`${C}api/net/config`,s).then(async d=>{d.ok}).finally(()=>{o.value=!1,t()})}}P(()=>{t()}),M(()=>{clearTimeout(y)});function w(l){return(l+99)*1.8}return(l,r)=>(n(),u("div",null,[f(m,{onClick:r[0]||(r[0]=s=>l.$router.go(-1)),label:"<<"}),r[3]||(r[3]=e("h2",{class:"ma-2"}," Network connection",-1)),e("div",Ie,[r[2]||(r[2]=e("div",{class:"list_files_ col-4 col-sm-12 _align-ic",style:{"padding-top":"8px"}}," Список доступных сетей: ",-1)),e("div",Pe,[f(m,{onClick:r[1]||(r[1]=s=>{Y(p)?p.value=1:p=1,t()}),label:"scan",loading:o.value,style:{width:"90px"}},null,8,["loading"]),(n(!0),u(j,null,T(a.value,s=>(n(),u("div",De,[e("div",null,_(i.value==s[0]?"*":"")+" "+_(s[0]),1),e("div",Ne,[e("div",{class:"progress",style:ee(`height:${w(s[3])}% ; width:${w(s[3])}% `)},null,4)]),e("div",null,[i.value==s[0]?(n(),u("a",{key:0,class:"cursor-p",onClick:c}," забыть ")):(n(),u("a",{key:1,class:"cursor-p",onClick:d=>h(s[0])}," подключить ",8,ze))])]))),256))])])]))}}),Me=D(Be,[["__scopeId","data-v-eb9d808e"]]),jt=Object.freeze(Object.defineProperty({__proto__:null,default:Me},Symbol.toStringTag,{value:"Module"})),Le={class:"row px-2",style:{"min-height":"5px"}},Je={class:"list_files row"},Ue={class:"col-4 col-md-6 col-sm-12 align-ic px-2"},Ke=["onClick"],Ae={class:"row pa-2",style:{"white-space":"break-spaces"}},Ee={class:"col-3 col-md-4 col-sm-6"},Fe={class:"text-b"},Ve={class:"col-3 col-md-4 col-sm-6"},Re={class:"text-b"},Ze={class:"col-3 col-md-4 col-sm-6"},Ge={class:"text-b"},qe=S({__name:"files",setup($){const a=k([]),i=k({used:null,free:null,total:null}),o=k(null),p=te(),y=k(!1);function t(w=""){y.value=!0,fetch(`${C}api/ls/${w}`).then(async l=>{if(l.ok){const r=await l.json();if(!r)return;a.value=r.files,i.value.free=r.free,i.value.total=r.total,i.value.used=r.used,o.value=r.currdir,console.log("api_data_74: ",a.value)}}).finally(()=>y.value=!1)}function c(w=""){confirm("Готовы удалить этот файл или папку?")&&fetch(`${C}api/delete/${w}`,{method:"delete"}).then(async l=>{l.ok?t():alert("Ошибка, что-то пошло не так...")}).catch(l=>alert("Ошибка, что-то пошло не так..."))}function h(w,l){l===16384&&t(`?chdir=${w}`),l===32768&&p.push({name:"show_content",query:{file_name:w}})}return P(()=>setTimeout(()=>{t()},9)),(w,l)=>(n(),u("div",null,[a.value.find(r=>r[0]=="/")?(n(),N(m,{key:0,onClick:l[0]||(l[0]=r=>h("/",16384)),label:"/",class:"mx-2"})):B("",!0),a.value.find(r=>r[0]=="..")?(n(),N(m,{key:1,onClick:l[1]||(l[1]=r=>h("..",16384)),label:"<<",class:"mx-2"})):B("",!0),f(m,{onClick:l[2]||(l[2]=r=>t()),label:"refresh",class:"mx-2"}),f(m,{_click:"set_params(r)",label:"upload",class:"mx-2"}),e("h3",null,"Current dir: "+_(o.value),1),e("div",Le,[e("div",{v_if:"loading",class:b(["loader",{loading:y.value}])},null,2)]),e("div",Je,[(n(!0),u(j,null,T(a.value,r=>(n(),u("div",Ue,[e("span",{class:b(["file_nm",{folder:r[1]==16384}]),onClick:s=>h(r[0],r[1])},_(r[0]),11,Ke),e("span",null,[f(m,{_click:"scan",onClick:s=>c(r[0]),label:"x"},null,8,["onClick"])])]))),256))]),e("div",Ae,[e("div",Ee,[l[3]||(l[3]=O(" total: ")),e("span",Fe,_(~~(i.value.total/100)/10)+" K",1)]),e("div",Ve,[l[4]||(l[4]=O(" free: ")),e("span",Re,_(~~(i.value.free/100)/10)+" K",1)]),e("div",Ze,[l[5]||(l[5]=O(" used: ")),e("span",Ge,_(~~(i.value.used/100)/10)+" K",1)])])]))}}),He=D(qe,[["__scopeId","data-v-4bc29d76"]]),Tt=Object.freeze(Object.defineProperty({__proto__:null,default:He},Symbol.toStringTag,{value:"Module"})),Qe={class:"row px-2",style:{"min-height":"5px"}},We={class:"list_files row px-2"},Xe=["textContent"],Ye=S({__name:"show_content",setup($){const a=k(null),i=G();let o=null;const p=k(!1);function y(t){p.value=!0,fetch(`${C}show_content/?file_name=${t}`).then(async c=>{if(c.ok){const h=await c.text();a.value=h,console.log("api_data_74: ","=",h.slice(0,11))}}).finally(c=>p.value=!1)}return P(()=>{o!==i.query.file_name&&(a.value=null,o=i.query.file_name,setTimeout(()=>{y(o)},9))}),(t,c)=>(n(),u("div",null,[f(m,{onClick:c[0]||(c[0]=h=>t.$router.go(-1)),label:"<<",class:"mx-2"}),e("h3",null,_(t.$route.query.file_name),1),e("div",Qe,[e("div",{v_show:"loading",class:b(["loader",{loading:p.value}])},null,2)]),e("div",We,[e("pre",{style:{"white-space":"pre-wrap","background-color":"#eeeeee",padding:"2px"},textContent:_(a.value)},null,8,Xe)])]))}}),et=D(Ye,[["__scopeId","data-v-2ed52032"]]),Ot=Object.freeze(Object.defineProperty({__proto__:null,default:et},Symbol.toStringTag,{value:"Module"})),tt={class:"row px-2"},lt={class:"col-6 col-md-12 px-2 _text-b align-ic"},st={class:"mx-2"},at=S({__name:"switches",setup($){const a=k(null);let i,o=0;function p(){i&&i.close(),i=new EventSource(`${C}api/switches/ls/?check_id=${o}`,{__withCredentials:!0,__heartbeatTimeout:12e4}),i.onmessage=t=>{try{const c=JSON.parse(t.data);o=t.lastEventId,a.value=c}catch(c){console.warn("evtSource_message_22: ",t.data.slice(0,4),t.data,c)}}}function y(t){const c={method:"put",body:JSON.stringify([{id:t.id,value:t.value}])};fetch(`${C}api/switches/set`,c).then(async h=>{h.ok})}return P(()=>{p()}),M(()=>{i&&i.close()}),(t,c)=>{var h,w;return n(),u("div",null,[f(m,{onClick:c[0]||(c[0]=l=>t.$router.go(-1)),label:"<<",class:"mx-2"}),c[1]||(c[1]=e("h3",null,"Switch view block ",-1)),e("div",tt,[(n(!0),u(j,null,T((h=a.value)==null?void 0:h.data,l=>(n(),u("div",lt,[f(m,{onClick:r=>{l.value=!l.value,y(l)},ladge:"",label:(l==null?void 0:l.name)||"switch"},{prepend:I(()=>[e("div",{class:b(["lamp",{on:l.value===1,off:l.value===0}]),_label:"switch"},null,2)]),_:2},1032,["onClick","label"]),e("div",{class:b(["lamp",{on:l.value===1,off:l.value===0}]),_label:"switch"},null,2),e("span",st,_(l.id)+" = "+_(l.value),1)]))),256))]),O(" tt: "+_((w=a.value)==null?void 0:w.time),1)])}}}),It=Object.freeze(Object.defineProperty({__proto__:null,default:at},Symbol.toStringTag,{value:"Module"})),ot={class:"row pa-2"},nt={class:"row pa-2"},it={class:"col-md-12 _col-4 px-2 text-b"},ct={class:"col-md-12_ _col-8 px-2"},rt={class:"row pa-md-2"},ut={class:"col-md-12 _col-6 pa-md-2",style:{"flex-grow":"1"}},dt={style:{overflow:"auto","max-width":"calc(100vw - 30px)"}},_t={class:"col-12 _px-2",style:{width:"600px"}},vt={class:"px-2"},ft={class:"col-md-12 _col-6 px-2",style:{"flex-grow":"1"}},pt={class:"col-12 pa-2 align-ic"},mt={class:"px-2"},ht={class:"col-12 _px-2 align-ic"},gt=S({__name:"cron_scheduler",setup($){const a=k(null);let i=null;const o=k(!1);function p(){o!=!0&&fetch(`${C}api/cron/ls`).then(async s=>{if(s.ok){const d=await s.json();a.value=d,o.value=!1}else sys_info.value=[]}).catch(s=>sys_info.value=[])}const y=J(()=>{var s;return((s=v.value)==null?void 0:s.datetime)&&new Date(v.value.datetime).toISOString().slice(8,16).replace("T"," ")});function t(s){a.value.tasks.push([!0,"- * * * *",s[0],s[2],s[1]])}function c(s){const d=prompt("Input schedule format [* * * * *] ",s[1]);d.trim().split(/\s+/).length==5&&(s[1]=d,o.value=!0)}function h(s){const d=prompt("Input params ",JSON.stringify(s[3]));if(d!==null){try{s[3]=JSON.parse(d)}catch{s[3]="params"}o.value=!0}}function w(s){const d=prompt("Input label ",s[4]);d!==null&&(s[4]=d,o.value=!0)}function l(){p()}P(()=>{i=!0,p()}),M(()=>{i=!1});function r(){const s={method:"put",body:JSON.stringify(a.value.tasks)};fetch(`${C}api/cron/set`,s).then(async d=>{d.ok&&p()}).catch(d=>{})}return U(()=>v.value.err,s=>{!s&&i&&p()}),(s,d)=>{var K,A,E;return n(),u("div",null,[d[5]||(d[5]=e("h3",null,"Scheduler",-1)),f(m,{onClick:d[0]||(d[0]=x=>s.$router.go(-1)),label:"<<",class:"mx-2"}),f(m,{onClick:d[1]||(d[1]=x=>{o.value=!1,l()}),label:"refresh"}),e("div",ot,[e("div",{class:b(["col-4 col-sm-6 pa-2 justify-cc",{"bg-warn":g(v).err}])}," UpTime: "+_(~~(g(v).uptime/60))+"min ",3),e("div",{class:b(["col-4 col-sm-12 pa-2 justify-cc",{"bg-warn":g(v).err}])}," PLC time: "+_(y.value),3)]),e("div",nt,[e("div",it,_((K=a.value)==null?void 0:K.name),1),e("div",ct,[e("div",rt,[e("div",ut,[d[2]||(d[2]=e("div",{class:"col-12 px-2"}," Рассписание: ",-1)),e("div",dt,[(n(!0),u(j,null,T((A=a.value)==null?void 0:A.tasks,(x,F)=>(n(),u("div",_t,[f(m,{class:b([x[0]?"_bg-positive":"bg-secondary"]),onClick:z=>{x[0]=!x[0],o.value=!0},label:x[0]?"o":"~",_label:"o"},null,8,["class","onClick","label"]),f(m,{onClick:z=>c(x),label:x[1]},null,8,["onClick","label"]),e("span",vt,_(x[2]),1),f(m,{onClick:z=>h(x),label:x[3]},null,8,["onClick","label"]),f(m,{onClick:z=>w(x),label:x[4]},null,8,["onClick","label"]),f(m,{onClick:z=>{a.value.tasks.splice(F,1),o.value=!0},label:"-"},null,8,["onClick"])]))),256))])]),e("div",ft,[e("div",pt,[d[3]||(d[3]=O(" Команды: ")),e("span",mt,[o.value?(n(),N(m,{key:0,onClick:r,label:"Save"})):B("",!0)])]),(n(!0),u(j,null,T((E=a.value)==null?void 0:E.cmd_list,(x,F)=>(n(),u("div",ht,[O(_(x)+" ",1),f(m,{onClick:z=>{t(x),o.value=!0},label:"+"},null,8,["onClick"])]))),256))])]),d[4]||(d[4]=O(' Schedule string: "* * * * *" as position "mm hh dw dd my" where: mm - minutes, hh - hours, dw - day of week, dd - day of month, my - month of year, format: every position may be * as any number; integer number; range of number 2-9; list 1,2,3; number with delimiter (example: */3 for every third), range with step throw delimiter 4-20/4 every fourth '))])])])}}}),Pt=Object.freeze(Object.defineProperty({__proto__:null,default:gt},Symbol.toStringTag,{value:"Module"})),yt={class:"row pa-2"},bt={class:"row pa-2"},$t=S({__name:"settings",setup($){const a=k(null);let i=null;function o(){fetch(`${C}api/status`).then(async t=>{if(t.ok){const c=await t.json();a.value=c}else a.value=[]}).catch(t=>a.value=[])}const p=J(()=>{var t;return((t=v.value)==null?void 0:t.datetime)&&new Date(v.value.datetime).toISOString().slice(8,16).replace("T"," ")});function y(){o()}return P(()=>{i=!0,o()}),M(()=>{i=!1}),U(()=>v.value.err,t=>{!t&&i&&o()}),(t,c)=>(n(),u("div",null,[f(m,{onClick:c[0]||(c[0]=h=>t.$router.go(-1)),label:"<<",class:"mx-2"}),f(m,{onClick:y,label:"refresh"}),c[2]||(c[2]=e("h3",null,"Settings - settings",-1)),e("div",yt,[e("div",{class:b(["col-3 col-sm-6 pa-2 justify-cc",{"bg-warn":g(v).err}])}," PLC time: "+_(p.value),3),e("div",{class:b(["col-3 col-sm-6 pa-2 justify-cc",{"bg-warn":g(v).err}])},"Free mem: "+_(~~(g(v).mem_free/100)/10)+"k",3),e("div",{class:b(["col-3 col-sm-6 pa-2 justify-cc",{"bg-warn":g(v).err}])},"UpTime: "+_(~~(g(v).uptime/60))+"min",3),e("div",{class:b(["col-3 col-sm-6 pa-2 justify-cc",{"bg-warn":g(v).err}])},"CPU load: "+_(~~(g(v).load*100+1))+"%",3)]),(n(!0),u(j,null,T(a.value,(h,w)=>(n(),u("div",bt,c[1]||(c[1]=[e("div",{class:"col-md-12 _col-4 px-2 _text-b"}," Page in dev mode ",-1)])))),256))]))}}),Dt=Object.freeze(Object.defineProperty({__proto__:null,default:$t},Symbol.toStringTag,{value:"Module"}));export{xt as L,D as _,v as a,C as b,It as c,Pt as d,Dt as e,Tt as f,Ct as h,St as i,jt as n,Ot as s};
