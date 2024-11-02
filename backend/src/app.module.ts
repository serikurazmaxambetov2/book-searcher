import { Module } from '@nestjs/common';
import { PrismaModule } from './prisma/prisma.module';
import { AcceptLanguageResolver, I18nModule } from 'nestjs-i18n';
import { join } from 'path';

@Module({
  imports: [
    PrismaModule,
    I18nModule.forRoot({
      fallbackLanguage: 'ru',
      loaderOptions: {
        path: join(__dirname, '/i18n/'),
        watch: true,
      },
      resolvers: [AcceptLanguageResolver],
    }),
  ],
})
export class AppModule {}
