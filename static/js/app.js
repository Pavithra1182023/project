window.AppUtil = window.AppUtil || {};
const storage = {
  get(key, fallback){
    try{ return JSON.parse(localStorage.getItem(key)) ?? fallback }catch{ return fallback }
  },
  set(key, value){ localStorage.setItem(key, JSON.stringify(value)) }
};

AppUtil.speak = function speak(text){
  if(!('speechSynthesis' in window)) return;
  const utter = new SpeechSynthesisUtterance(text);
  utter.rate = 0.95; utter.pitch = 1.0;
  window.speechSynthesis.speak(utter);
}

AppUtil.saveResult = function saveResult(entry){
  const history = storage.get('history', []);
  history.push({ ...entry, timestamp: Date.now() });
  storage.set('history', history);
}

AppUtil.getHistory = function getHistory(){
  return storage.get('history', []);
}

AppUtil.average = function average(numbers){
  if(numbers.length === 0) return 0;
  return numbers.reduce((a,b)=>a+b,0)/numbers.length;
}

AppUtil.guid = function guid(){
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}
