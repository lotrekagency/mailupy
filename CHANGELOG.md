# CHANGELOG



## v1.1.3 (2024-01-17)

### Fix

* fix(client): handling more than 20 items in get_fields ([`ab36307`](https://github.com/lotrekagency/mailupy/commit/ab36307aa963de85d35c088a96a34ee27b3a1207))

* fix(exceptions): full response.json() in exception ([`78bb6bd`](https://github.com/lotrekagency/mailupy/commit/78bb6bdb7892284fa6bd8c551d4433c476f3a757))

### Unknown

* Merge pull request #8 from lotrekagency/fix/missing-error-description

Fix/missing error description ([`60d57ad`](https://github.com/lotrekagency/mailupy/commit/60d57adf18e0e695c106202bcafcfe3d14fc4e43))

* Merge remote-tracking branch &#39;origin/master&#39; into fix/missing-error-description ([`1197116`](https://github.com/lotrekagency/mailupy/commit/11971169c3fc8d147092646299ca7853852df995))


## v1.1.2 (2024-01-16)

### Chore

* chore: remove pypi url from CD workflow ([`6f9e3b7`](https://github.com/lotrekagency/mailupy/commit/6f9e3b736eb4d0ac83cff6a5e5560cfb453d00a5))

* chore: pass secret token to pypi upload ([`2e27d41`](https://github.com/lotrekagency/mailupy/commit/2e27d414aad11f67133bdb8725bcc33ba178b8a1))

### Fix

* fix: fix _download_all_pages handler ([`f72d09d`](https://github.com/lotrekagency/mailupy/commit/f72d09d09d267375eb9fe8dbb39875384338a366))

### Unknown

* Merge branch &#39;master&#39; of github.com:lotrekagency/mailupy ([`b5b04d0`](https://github.com/lotrekagency/mailupy/commit/b5b04d07b63e3d71c575fb61a09ad63758996436))


## v1.1.1 (2024-01-16)

### Chore

* chore: fix semantic release cong ([`b87e5eb`](https://github.com/lotrekagency/mailupy/commit/b87e5eba4481f1e214b8e73a0b591aa958f20cc7))

* chore: update ci cd and release structure ([`92d2c2e`](https://github.com/lotrekagency/mailupy/commit/92d2c2e447781578adf8170af12d9f0434922252))

* chore: remove sudo from twine upload command ([`049ff9d`](https://github.com/lotrekagency/mailupy/commit/049ff9dac1a70822a09088dd5ad796868a9650ff))

* chore: version 1.1.1 ([`9b41ce6`](https://github.com/lotrekagency/mailupy/commit/9b41ce64f7d72d6b0c6f348b69ad5bd350e15d88))

* chore: updated cd.yml ([`79b49d1`](https://github.com/lotrekagency/mailupy/commit/79b49d103bdbf5846687e9d96560295c5ce8898d))

* chore: added ci.yml ([`16a796a`](https://github.com/lotrekagency/mailupy/commit/16a796a5721ced9d5126dee2e885a2d240001e82))

* chore: generate coverage xml ([`cda3870`](https://github.com/lotrekagency/mailupy/commit/cda3870d46640172c9a144cfa7ba32c9eb48d609))

* chore: updated ci.yml ([`215831f`](https://github.com/lotrekagency/mailupy/commit/215831f2f97fe5fc831d61069e6198df6d061c48))

* chore: updated ci.yml ([`f3fb419`](https://github.com/lotrekagency/mailupy/commit/f3fb419ea57daa4e11da637acade45daed8e8bc6))

* chore: added ci.yml ([`e60e3a0`](https://github.com/lotrekagency/mailupy/commit/e60e3a0834617996787ceee9b43b789bf598a7c0))

### Fix

* fix(exceptions): using get() method while getting ErrorDescription key in exceptions ([`e3165fc`](https://github.com/lotrekagency/mailupy/commit/e3165fca56882fbbdb2af3aa72689899aa6b6f67))

* fix: round up to highest integer in page counter ([`1ab8bf0`](https://github.com/lotrekagency/mailupy/commit/1ab8bf01d2892db646b963b9fa75c417d76bb4d1))

### Test

* test: fix sms mock ([`2d3ec04`](https://github.com/lotrekagency/mailupy/commit/2d3ec0405b59bef2c68e020f99b4599ffa4564fc))

### Unknown

* Merge pull request #7 from lotrekagency/fix/missing-error-description

fix(exceptions): using get() method while getting ErrorDescription ke… ([`ec3ce7c`](https://github.com/lotrekagency/mailupy/commit/ec3ce7c7d49a60bb93fd7c3e19691fa7d295218a))

* Merge pull request #3 from mino89/master

Send Sms message method implemented ([`6e04e9d`](https://github.com/lotrekagency/mailupy/commit/6e04e9d9f68b1f91aa61ef886b9836ec7e479216))

* replaced fake telephone number and added fields parameters to send mail and sms ([`aa32942`](https://github.com/lotrekagency/mailupy/commit/aa329425fbcb67d8bf24ca6d4f82faf65f1f76c9))

* fixed refuse in comments ([`e5be6a0`](https://github.com/lotrekagency/mailupy/commit/e5be6a00415b9fcc8ed35c6771c761ede80aa193))

* implemented sms send method ([`40571b3`](https://github.com/lotrekagency/mailupy/commit/40571b3e92a25df8cddbec23354c67e7df17416d))


## v1.1.0 (2020-07-23)

### Unknown

* Version 1.1.0 ([`87754d7`](https://github.com/lotrekagency/mailupy/commit/87754d72e7957ee2a6bc39301286050ad19fd578))

* Upgrade requests module to 2.24.0 ([`3fea735`](https://github.com/lotrekagency/mailupy/commit/3fea735b8d7c3cb5b81d0b56243be78da09d7515))

* Add contributors section ([`9885091`](https://github.com/lotrekagency/mailupy/commit/9885091771df61926051a858401f414ff3e85d4b))

* Add &#39;pending&#39; attribute to subscribe_to_list doc ([`cc94667`](https://github.com/lotrekagency/mailupy/commit/cc94667c7bd6a63fd82030d1930e46523c273bc0))

* Merge pull request #2 from Arussil/master

Added parameter for subscribe a user in &#34;pending&#34; status ([`1af180a`](https://github.com/lotrekagency/mailupy/commit/1af180ab730f878ae2900c0dac1ee896d043456e))

* Added parameter for subscribe a user in &#34;pending&#34; status ([`0c59c76`](https://github.com/lotrekagency/mailupy/commit/0c59c7688839606bc11209dce49a46b4edfac4a1))

* Write docs ([`12bfc63`](https://github.com/lotrekagency/mailupy/commit/12bfc630f61159f78500a882adc5bedf14439b9d))

* Flake8 before docs ([`3adf262`](https://github.com/lotrekagency/mailupy/commit/3adf262343b00d4da8b48d74b55fe0c532ffe7f4))


## v1.0.0 (2020-02-07)

### Unknown

* Version 1.0.0 ([`28cc65e`](https://github.com/lotrekagency/mailupy/commit/28cc65e92fc2c5194838f484252bdd4291d2877c))

* Use &#39;recipient&#39; instead of &#39;user&#39; ([`f4b2383`](https://github.com/lotrekagency/mailupy/commit/f4b23830a7c7fcd649eb11c75d7dc0fa4cd6cc89))

* Update README with examples ([`7ee1953`](https://github.com/lotrekagency/mailupy/commit/7ee1953cff64d6c29d5e6493f5210ad9fb46f5d7))

* Fix README ([`4ec7d54`](https://github.com/lotrekagency/mailupy/commit/4ec7d5498930e62b95429b545f8553e78cf84af9))

* Remove useless pagination code ([`1b8f061`](https://github.com/lotrekagency/mailupy/commit/1b8f06183cd236952cdf8f295a94ddd3c0d73de0))

* Now not safe methods throws exceptions ([`6539569`](https://github.com/lotrekagency/mailupy/commit/6539569d197d1a16f5715c7ddb68844595e26be5))

* Huge refactoring with generators ([`6e5a481`](https://github.com/lotrekagency/mailupy/commit/6e5a481a071ab41ac23ee48565c5c7f0bfa3d4e9))

* Reorganize code ([`31f3cab`](https://github.com/lotrekagency/mailupy/commit/31f3cababdac51c9b62967d978d278ee2be7dab8))

* Add docs ([`04334df`](https://github.com/lotrekagency/mailupy/commit/04334df2c2c92e086bdf4bd1a52233832156d747))

* Add MailUp credits ([`4e44390`](https://github.com/lotrekagency/mailupy/commit/4e44390b6eac49fc70f9617159dd07a8612f8356))

* Add 💌 ([`437f0de`](https://github.com/lotrekagency/mailupy/commit/437f0de2d572586adccc5bc7090061f9fabf2a8a))

* Add badges ([`1aebd46`](https://github.com/lotrekagency/mailupy/commit/1aebd4601e17d33564c07cc12859dfd191c5e56f))

* Update flake8 ([`981b64c`](https://github.com/lotrekagency/mailupy/commit/981b64c7b5d397aed5c533f18eb4eaed4d2dbca0))

* Fix python and libraries versions ([`37adf43`](https://github.com/lotrekagency/mailupy/commit/37adf436f549b44ca7c348ce3c4902723215e335))

* Merge remote-tracking branch &#39;origin/feature/various_fixes&#39; ([`0f67679`](https://github.com/lotrekagency/mailupy/commit/0f6767954c58d0d1d283282713745695a916355a))

* Added tests, custom exception and auto-login on token expiration ([`2ae1d30`](https://github.com/lotrekagency/mailupy/commit/2ae1d30fa6e8a55bcb317951ef719e911e64bb3a))

* Update LICENSE ([`4656593`](https://github.com/lotrekagency/mailupy/commit/4656593ff0b87cadd4302f509afd0967df4a639d))

* Autologin by default ([`931fc37`](https://github.com/lotrekagency/mailupy/commit/931fc373945a9450c775bf2327ffa8503397a921))

* Remove useless code ([`b32fe72`](https://github.com/lotrekagency/mailupy/commit/b32fe7227208a9cc3194f71a0b5e87ccc925d870))

* First import ([`af992fa`](https://github.com/lotrekagency/mailupy/commit/af992fa2bed1c333405151627c7affbd599ae5ae))
