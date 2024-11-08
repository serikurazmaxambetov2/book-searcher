import { Module } from '@nestjs/common';
import { PrismaModule } from './prisma/prisma.module';
import { BookModule } from './book/book.module';
import { AcceptLanguageResolver, I18nModule } from 'nestjs-i18n';
import { join } from 'path';
import { SearchModule } from './search/search.module';

@Module({
  imports: [
    PrismaModule,
    BookModule,
    I18nModule.forRoot({
      fallbackLanguage: 'ru',
      loaderOptions: {
        path: join(__dirname, '/i18n/'),
        watch: true,
      },
      resolvers: [AcceptLanguageResolver],
    }),
    SearchModule,
  ],
})
export class AppModule {}
