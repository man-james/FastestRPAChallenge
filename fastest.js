let form=document.querySelector('body div.inputFields > form');
let b=form.querySelector('.btn.uiColorButton');
let d0={labelAddress:'98 North Road',labelCompanyName:'IT Solutions',labelLastName:'Smith',labelFirstName:'John',labelEmail:'jsmith@itsolutions.co.uk',labelPhone:'40716543298',labelRole:'Analyst'}
let d1={labelAddress:'11 Crown Street',labelCompanyName:'MediCare',labelLastName:'Dorsey',labelFirstName:'Jane',labelEmail:'jdorsey@mc.com',labelPhone:'40791345621',labelRole:'Medical Engineer'}
let d2={labelAddress:'22 Guild Street',labelCompanyName:'Waterfront',labelLastName:'Kipling',labelFirstName:'Albert',labelEmail:'kipling@waterfront.com',labelPhone:'40735416854',labelRole:'Accountant'}
let d3={labelAddress:'17 Farburn Terrace',labelCompanyName:'MediCare',labelLastName:'Robertson',labelFirstName:'Michael',labelEmail:'mrobertson@mc.com',labelPhone:'40733652145',labelRole:'IT Specialist'}
let d4={labelAddress:'99 Shire Oak Road',labelCompanyName:'Timepath Inc.',labelLastName:'Derrick',labelFirstName:'Doug',labelEmail:'dderrick@timepath.co.uk',labelPhone:'40799885412',labelRole:'Analyst'}
let d5={labelAddress:'27 Cheshire Street',labelCompanyName:'Aperture Inc.',labelLastName:'Marlowe',labelFirstName:'Jessie',labelEmail:'jmarlowe@aperture.us',labelPhone:'40733154268',labelRole:'Scientist'}
let d6={labelAddress:'10 Dam Road',labelCompanyName:'Sugarwell',labelLastName:'Hamm',labelFirstName:'Stan',labelEmail:'shamm@sugarwell.org',labelPhone:'40712462257',labelRole:'Advisor'}
let d7={labelAddress:'13 White Rabbit Street',labelCompanyName:'Aperture Inc.',labelLastName:'Norton',labelFirstName:'Michelle',labelEmail:'mnorton@aperture.us',labelPhone:'40731254562',labelRole:'Scientist'}
let d8={labelAddress:'19 Pineapple Boulevard',labelCompanyName:'TechDev',labelLastName:'Shelby',labelFirstName:'Stacy',labelEmail:'sshelby@techdev.com',labelPhone:'40741785214',labelRole:'HR Manager'}
let d9={labelAddress:'87 Orange Street',labelCompanyName:'Timepath Inc.',labelLastName:'Palmer',labelFirstName:'Lara',labelEmail:'lpalmer@timepath.co.uk',labelPhone:'40731653845',labelRole:'Programmer'}
let ci = ng.probe(b).componentInstance;
ci.start();
let l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d0[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d1[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d2[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d3[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d4[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d5[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d6[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d7[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d8[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d9[i.getAttribute('ng-reflect-name')];});
b.click();
